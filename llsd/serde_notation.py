import base64
import binascii
import uuid

from llsd.base import (_LLSD, B, LLSDBaseFormatter, LLSDBaseParser, NOTATION_HEADER,
                       LLSDParseError, LLSDSerializationError, UnicodeType,
                       _format_datestr, _parse_datestr, _str_to_bytes, binary, uri, PY2)

if not PY2:
    STR_ESC_TRANS_SINGLE = str.maketrans({'\\': '\\\\',
                                          '\'':'\\\''})
    STR_ESC_TRANS_DOUBLE = str.maketrans({'\\': '\\\\',
                                          '\"':'\\\"'})


class LLSDNotationParser(LLSDBaseParser):
    """
    Parse LLSD notation.

    See http://wiki.secondlife.com/wiki/LLSD#Notation_Serialization

    * map: { string:object, string:object }
    * array: [ object, object, object ]
    * undef: !
    * boolean: true | false | 1 | 0 | T | F | t | f | TRUE | FALSE
    * integer: i####
    * real: r####
    * uuid: u####
    * string: "g\'day" | 'have a "nice" day' | s(size)"raw data"
    * uri: l"escaped"
    * date: d"YYYY-MM-DDTHH:MM:SS.FFZ"
    * binary: b##"ff3120ab1" | b(size)"raw data"
    """
    def __init__(self):
        super(LLSDNotationParser, self).__init__()
        # Like LLSDBinaryParser, we want to dispatch based on the current
        # character.
        _dispatch_dict = {
            # map
            b'{': self._parse_map,
            # array
            b'[': self._parse_array,
            # undefined
            b'!': lambda cc: None,
            # false
            b'0': lambda cc: False,
            # true
            b'1': lambda cc: True,
            # false, must check for F|f|false|FALSE
            b'F': self._parse_false,
            b'f': self._parse_false,
            # true, must check for T|t|true|TRUE
            b'T': self._parse_true,
            b't': self._parse_true,
            # 'i' = integer
            b'i': self._parse_integer,
            # 'r' = real number
            b'r': self._parse_real,
            # 'u' = uuid
            b'u': self._parse_uuid,
            # string
            b"'": self._parse_string,
            b'"': self._parse_string,
            b's': self._parse_string,
            # 'l' = uri
            b'l': self._parse_uri,
            # 'd' = date in seconds since epoch
            b'd': self._parse_date,
            # 'b' = binary
            b'b': self._parse_binary,
            }
        # Like LLSDBinaryParser, construct a lookup list from this dict. Start
        # by filling with the 'else' case.
        self._dispatch = 256*[lambda cc: self._error("Invalid notation token")]
        # Then fill in specific entries based on the dict above.
        for c, func in _dispatch_dict.items():
            self._dispatch[ord(c)] = func

    def parse(self, something, ignore_binary = False):
        """
        This is the basic public interface for parsing.

        :param something: serialized LLSD to parse: a bytes object, a binary
                          stream or an LLSDBaseParser subclass.
        :param ignore_binary: parser throws away data in llsd binary nodes.
        :returns: returns a python object.
        """
        self._reset(something)

        # EOF is an acceptable result
        cc = self._getc(full=False)
        # special case for notation: empty input means False
        if not cc:
            return False

        return self._parse(cc)

    def _get_until(self, delim):
        content = []
        try:
            c = self._getc()
            while c != delim:
                content.append(c)
                c = self._getc()
        except LLSDParseError:
            # traditionally this function returns None when there's no
            # subsequent delim within the input buffer
            return None
        else:
            # we've already consumed the close delim
            return b''.join(content)

    def _parse(self, cc):
        "The notation parser workhorse."
        try:
            func = self._dispatch[ord(cc)]
        except IndexError:
            # output error if the token was out of range
            self._error("Invalid notation token")
        else:
            # pass the lookahead character that selected this func
            return func(cc)

    def _parse_binary(self, cc):
        "parse a single binary object."

        # skip the beginning 'b'
        cc = self._getc()
        if cc == b'(':
            # parse raw binary
            # grab the 'expected' size of the binary data
            size = self._get_until(b')')
            if size == None:
                self._error("Invalid binary size")
            size = int(size)

            # grab the opening quote
            q = self._getc()
            if q != b'"':
                self._error('Expected " to start binary value')

            # grab the data
            data = self._getc(size)

            # grab the closing quote
            q = self._getc()
            if q != b'"':
                self._error('Expected " to end binary value')

            return binary(data)

        else:
            # get the encoding base
            base = cc + self._getc()
            try:
                decoder = {
                    b'16': base64.b16decode,
                    b'64': base64.b64decode,
                    }[base]
            except KeyError:
                self._error("Parser doesn't support base %s encoding" %
                            base.decode('latin-1'))

            # grab the double quote
            q = self._getc()
            if q != b'"':
                self._error('Expected " to start binary value')

            # grab the encoded data
            encoded = self._get_until(q)

            try:
                return binary(decoder(encoded or b''))
            except binascii.Error as exc:
                # convert exception class so it's more catchable
                self._error("Encoded binary data: " + str(exc))
            except TypeError as exc:
                # convert exception class so it's more catchable
                self._error("Bad binary data: " + str(exc))

    def _parse_map(self, cc):
        """
        parse a single map

        map: { string:object, string:object }
        """
        rv = {}
        key = b''
        found_key = False
        # skip the beginning '{'
        cc = self._getc()
        while (cc != b'}'):
            if cc is None:
                self._error("Unclosed map")
            if not found_key:
                if cc in (b"'", b'"', b's'):
                    key = self._parse_string(cc)
                    found_key = True
                elif cc.isspace() or cc == b',':
                    # ignore space or comma
                    pass
                else:
                    self._error("Invalid map key")
            elif cc.isspace():
                # ignore space
                pass
            elif cc == b':':
                # skip the ':'
                value = self._parse(self._getc())
                rv[key] = value
                found_key = False
            else:
                self._error("missing separator")
            cc = self._getc()

        return rv

    def _parse_array(self, cc):
        """
        parse a single array.

        array: [ object, object, object ]
        """
        rv = []
        # skip the beginning '['
        cc = self._getc()
        while (cc != b']'):
            if cc is None:
                self._error('Unclosed array')
            if cc.isspace() or cc == b',':
                cc = self._getc()
                continue
            rv.append(self._parse(cc))
            cc = self._getc()

        return rv

    def _parse_uuid(self, cc):
        "Parse a uuid."
        # ignore the beginning 'u'
        # see comment on LLSDNotationFormatter._UUID() re use of latin-1
        return uuid.UUID(hex=self._getc(36).decode('latin-1'))

    def _parse_uri(self, cc):
        "Parse a URI."
        # skip the beginning 'l'
        return uri(self._parse_string(self._getc()))

    def _parse_date(self, cc):
        "Parse a date."
        # skip the beginning 'd'
        datestr = self._parse_string(self._getc())
        return _parse_datestr(datestr)

    def _parse_real(self, cc):
        "Parse a floating point number."
        # recognize:
        # [+-]?inf
        # [+-]?nan
        # [+-]?basepart([eE][+-]?\d+)?
        # where basepart could be either:
        # \d+(\.\d*)? or
        # \d*\.\d+
        digits = []
        # skip the beginning 'r'
        cc = self._collect_sign(self._getc(), digits)
        try:
            rest = {b'i': b'nf', b'n': b'an'}[cc]
        except KeyError:
            # cc is neither 'i' nor 'n', must be a digit:
            # collect integer digits
            idigits = []
            fdigits = []
            edigits = []
            cc = self._collect_digits(cc, idigits)
            digits.extend(idigits)
            if cc == b'.':
                digits.append(cc)
                # skip decimal point and collect fractional digits
                cc = self._collect_digits(self._getc(full=False), fdigits)
                digits.extend(fdigits)
            # Fun fact: (cc in b'eE') is True even when cc is b''!
            if cc in (b'e', b'E'):
                digits.append(cc)
                # skip 'e' and check for exponent sign
                cc = self._collect_sign(self._getc(), digits)
                cc = self._collect_digits(cc, edigits)
                digits.extend(edigits)
                if not edigits:
                    # if 'e' is present, there MUST be an exponent
                    self._error('Invalid real exponent')
            # Whether this real number ended after the integer part, after the
            # decimal point, after the fractional part or after the exponent,
            # cc is now one character PAST the end -- put it back.
            self._putback(cc)
            # The reason we collected idigits and fdigits separately is that
            # while either may be empty, they may not BOTH be empty.
            if not (idigits or fdigits):
                self._error('Invalid real number')
        else:
            # cc is either 'i' for 'inf' or 'n' for 'nan',
            # rest is 'nf' or 'an'
            digits.extend([cc, self._expect(cc + rest, rest)])

        return float(b''.join(digits))

    def _parse_integer(self, cc):
        "Parse an integer."
        digits = []
        # skip the beginning 'i'
        cc = self._collect_sign(self._getc(), digits)
        cc = self._collect_digits(cc, digits)
        if not digits:
            self._error('Invalid integer token')

        # cc is now the next _getc() after the last digit -- back up
        self._putback(cc)

        return int(b''.join(digits))

    def _collect_sign(self, cc, digits):
        if cc in (b'+', b'-'):
            digits.append(cc)
            cc = self._getc()
        return cc

    def _collect_digits(self, cc, digits):
        while cc.isdigit():
            digits.append(cc)
            # we can accept EOF happening here
            cc = self._getc(full=False)
        return cc

    def _parse_string(self, delim):
        """
        Parse a string

        string: "g\'day" | 'have a "nice" day' | s(size)"raw data"
        """
        rv = ""
        if delim in (b"'", b'"'):
            rv = self._parse_string_delim(delim)
        elif delim == b's':
            rv = self._parse_string_raw()
        else:
            self._error("invalid string token")

        return rv

    def _parse_string_raw(self):
        """
        Parse a sized specified string.

        string: s(size)"raw data"
        """
        # Read the (size) portion.
        cc = self._getc()
        if cc != b'(':
            self._error("Invalid string token")

        size = self._get_until(b')')
        if size == None:
            self._error("Invalid string size")
        size = int(size)

        delim = self._getc()
        if delim not in (b"'", b'"'):
            self._error("Invalid string token")

        rv = self._getc(size)
        cc = self._getc()
        if cc != delim:
            self._error("Invalid string closure token")
        try:
            return rv.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise LLSDParseError(exc)

    def _parse_true(self, cc):
        # match t, T, true, TRUE -- not mixed-case
        return self._parse_bool(cc, True, (b'true', b'TRUE'))

    def _parse_false(self, cc):
        # match f, F, false, FALSE -- not mixed-case
        return self._parse_bool(cc, False, (b'false', b'FALSE'))

    def _parse_bool(self, cc, result, tokens):
        try:
            # Index on first character to find expected rest.
            # Beware, token is bytes, so token[0] is an int!
            rest = {token[:1]: token[1:] for token in tokens}[cc]
        except KeyError:
            self._error("Invalid '%s' token" % tokens[0])

        cc = self._getc(full=False)
        if cc != rest[:1]:
            # legal to have only first char, put back cc and carry on
            self._putback(cc)
            return result

        # saw 'tr' or 'TR' (or 'fa' or 'FA'), cc is the second char:
        # MUST be followed by the rest of 'rest'
        self._expect(tokens[0], rest[1:])
        return result

    def _expect(self, token, match):
        # verify that the next several chars are exactly what we expect
        if self._getc(len(match), full=False) != match:
            self._error("Invalid '%s' token" % token)
        return match


class LLSDNotationFormatter(LLSDBaseFormatter):
    """
    Serialize a python object as application/llsd+notation

    See http://wiki.secondlife.com/wiki/LLSD#Notation_Serialization
    """
    def _LLSD(self, v):
        raise LLSDSerializationError("We should never end up here") # pragma: no cover
    def _UNDEF(self, v):
        return b'!'
    def _BOOLEAN(self, v):
        return b'true' if v else b'false'
    def _INTEGER(self, v):
        return B("i%d") % v
    def _REAL(self, v):
        return B("r%r") % v
    def _UUID(self, v):
        # latin-1 is the byte-to-byte encoding, mapping \x00-\xFF ->
        # \u0000-\u00FF. It's also the fastest encoding, I believe, from
        # https://docs.python.org/3/library/codecs.html#encodings-and-unicode
        # UUID doesn't like the hex to be a bytes object, so I have to
        # convert it to a string. I chose latin-1 to exactly match the old
        # error behavior in case someone passes an invalid hex string, with
        # things other than 0-9a-fA-F, so that they will fail in the UUID
        # decode, rather than with a UnicodeError.
        return b"u" + str(v).encode('latin-1')
    def _BINARY(self, v):
        return b'b64"' +  base64.b64encode(v).strip() + b'"'

    def _STRING(self, v):
        if self.py2: # pragma: no cover
            return b"'" + self._esc(v) + b"'"
        return b"'" + v.translate(STR_ESC_TRANS_SINGLE).encode('utf-8') + b"'"
    def _URI(self, v):
        if self.py2: # pragma: no cover
            return  b'l"' + self._esc(v, b'"') + b'"'
        return  b'l"' + v.translate(STR_ESC_TRANS_DOUBLE).encode('utf-8') + b'"'
    def _DATE(self, v):
        return b'd"' + _format_datestr(v) + b'"'
    def _ARRAY(self, v):
        raise LLSDSerializationError("We should never end up here") # pragma: no cover
    def _MAP(self, v):
        raise LLSDSerializationError("We should never end up here") # pragma: no cover
    def _esc(self, data, quote=b"'"):
        return _str_to_bytes(data).replace(b"\\", b"\\\\").replace(quote, b'\\'+quote)

    def _write(self, something):
        """
        Serialize a python object to self.stream as application/llsd+notation.

        :param something: A python object (typically a dict) to be serialized.

        NOTE: This is nearly identical to the above _write with the exception
        that this one includes newlines and indentation.  Doing something clever
        for the above may decrease performance for the common case, so it's been
        split out.  We can probably revisit this, though.
        """

        iter_stack = [[iter([something]), b"", None, b""]]
        while True:
            cur_iter, iter_type, iterable_obj, delim = iter_stack[-1]
            try:
                item = next(cur_iter)
                self.stream.write(delim)
                iter_stack[-1][3] = b","
                if iter_type == b"}":
                    if self.py2:  # pragma: no cover
                        self.stream.writelines([b"'", self._esc(UnicodeType(item)), b"':"])
                    else:
                        # calling translate directly is a bit faster
                        self.stream.writelines([b"'",
                                                UnicodeType(item).translate(STR_ESC_TRANS_SINGLE).encode('utf-8'),
                                                b"':"])
                    item = iterable_obj[item] # pylint: disable=unsubscriptable-object
                if isinstance(item, _LLSD):
                    item = item.thing
                item_type = type(item)
                if not item_type in self.type_map:
                    raise LLSDSerializationError(
                        "Cannot serialize unknown type: %s (%s)" % (item_type, item))
                tfunction = self.type_map[item_type]

                if tfunction == self._MAP:
                    self.stream.write(b'{')
                    iter_stack.append([iter(list(item)), b"}", item, b""])
                elif tfunction == self._ARRAY:
                    self.stream.write(b'[')
                    iter_stack.append([iter(item), b"]", None, b""])
                else:
                    self.stream.write(tfunction(item))
            except StopIteration:
                self.stream.write(iter_type)
                iter_stack.pop()
            if len(iter_stack) == 1:
                break


def format_notation(something):
    """
    Format a python object as application/llsd+notation

    :param something: a python object (typically a dict) to be serialized.
    :returns: Returns a LLSD notation formatted string.

    See http://wiki.secondlife.com/wiki/LLSD#Notation_Serialization
    """
    return LLSDNotationFormatter().format(something)


def write_notation(stream, something):
    """
    Serialize to passed binary 'stream' a python object 'something' as
    application/llsd+notation.

    :param stream: a binary stream open for writing.
    :param something: a python object (typically a dict) to be serialized.

    See http://wiki.secondlife.com/wiki/LLSD#Notation_Serialization
    """
    return LLSDNotationFormatter().write(stream, something)


def parse_notation(something):
    """
    This is the basic public interface for parsing llsd+notation.

    :param something: The data to parse.
    :returns: Returns a python object.
    """
    # Try to match header, and if matched, skip past it.
    parser = LLSDBaseParser(something)
    parser.matchseq(NOTATION_HEADER)
    # If we matched the header, then parse whatever follows, else parse the
    # original bytes object or stream.
    return parse_notation_nohdr(parser)


def parse_notation_nohdr(baseparser):
    """
    Parse llsd+notation known to be without a header.

    :param baseparser: LLSDBaseParser instance wrapping the data to parse.
    :returns: Returns a python object.
    """
    return LLSDNotationParser().parse(baseparser)
