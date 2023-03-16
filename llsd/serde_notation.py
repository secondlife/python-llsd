import base64
import binascii
import re
import uuid

from llsd.base import (_LLSD, B, LLSDBaseFormatter, LLSDBaseParser, NOTATION_HEADER,
                       LLSDParseError, LLSDSerializationError, UnicodeType,
                       _format_datestr, _parse_datestr, _str_to_bytes, binary, uri)

_real_regex = re.compile(br"[-+]?(?:(\d+(\.\d*)?|\d*\.\d+)([eE][-+]?\d+)?)|[-+]?inf|[-+]?nan")
_true_regex = re.compile(br"TRUE|true|\b[Tt]\b")
_false_regex = re.compile(br"FALSE|false|\b[Ff]\b")


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

    def parse(self, baseparser, ignore_binary = False):
        """
        This is the basic public interface for parsing.

        :param baseparser: LLSDBaseParser or subclass holding data to parse.
        :param ignore_binary: parser throws away data in llsd binary nodes.
        :returns: returns a python object.
        """
        self._reset(baseparser)

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

    def _get_re(self, cc, desc, regex, override=None):
        # This is the case for which we introduced _peek(full=False).
        # Instead of trying to reimplement each of the re patterns passed to
        # this method as individual operations on _stream, peek ahead by a
        # reasonable amount and directly use re. full=False means we're
        # willing to accept a result buffer shorter than our lookahead.
        # Don't forget to prepend our lookahead character.
        # You would think we could parse real, True or False with fewer bytes
        # than this, but fuzz testing produces some real humdinger float
        # values.
        peek = cc + self._peek(30, full=False)
        match = regex.match(peek)
        if not match:
            self._error("Invalid %s token" % desc)
        else:
            # skip what we matched, adjusting for the char we already read
            self._getc(match.end() - len(cc))
            return override if override is not None else match.group(0)

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
        # see comment on LLSDNotationFormatter.UUID() re use of latin-1
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
        # ignore the beginning 'r'
        return float(self._get_re(b'', "real", _real_regex))

    def _parse_integer(self, cc):
        "Parse an integer."
        # ignore the beginning 'i'
        cc = self._getc()
        sign = 1
        if cc == b'+':
            cc = self._getc()
        elif cc == b'-':
            sign = -1
            cc = self._getc()

        digits = []
        while cc.isdigit():
            digits.append(cc)
            # we can accept EOF happening here
            cc = self._getc(full=False)

        # cc is now the next _getc() after the last digit -- back up
        if cc:
            self._putback()

        if not digits:
            self._error('Invalid integer token')

        return sign * int(b''.join(digits))

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
        return self._get_re(cc, "'true'", _true_regex, True)

    def _parse_false(self, cc):
        return self._get_re(cc, "'false'", _false_regex, False)


class LLSDNotationFormatter(LLSDBaseFormatter):
    """
    Serialize a python object as application/llsd+notation

    See http://wiki.secondlife.com/wiki/LLSD#Notation_Serialization
    """
    __slots__ = []

    def LLSD(self, v):
        return self._generate(v.thing)
    def UNDEF(self, v):
        return b'!'
    def BOOLEAN(self, v):
        if v:
            return b'true'
        else:
            return b'false'
    def INTEGER(self, v):
        return B("i%d") % v
    def REAL(self, v):
        return B("r%r") % v
    def UUID(self, v):
        # latin-1 is the byte-to-byte encoding, mapping \x00-\xFF ->
        # \u0000-\u00FF. It's also the fastest encoding, I believe, from
        # https://docs.python.org/3/library/codecs.html#encodings-and-unicode
        # UUID doesn't like the hex to be a bytes object, so I have to
        # convert it to a string. I chose latin-1 to exactly match the old
        # error behavior in case someone passes an invalid hex string, with
        # things other than 0-9a-fA-F, so that they will fail in the UUID
        # decode, rather than with a UnicodeError.
        return B("u%s") % str(v).encode('latin-1')
    def BINARY(self, v):
        return b'b64"' + base64.b64encode(v).strip() + b'"'

    def STRING(self, v):
        return B("'%s'") % _str_to_bytes(v).replace(b"\\", b"\\\\").replace(b"'", b"\\'")
    def URI(self, v):
        return B('l"%s"') % _str_to_bytes(v).replace(b"\\", b"\\\\").replace(b'"', b'\\"')
    def DATE(self, v):
        return B('d"%s"') % _format_datestr(v)
    def ARRAY(self, v):
        return B("[%s]") % b','.join([self._generate(item) for item in v])
    def MAP(self, v):
        return B("{%s}") % b','.join([B("'%s':%s") % (_str_to_bytes(UnicodeType(key)).replace(b"\\", b"\\\\").replace(b"'", b"\\'"), self._generate(value))
             for key, value in v.items()])

    def _generate(self, something):
        "Generate notation from a single python object."
        t = type(something)
        handler = self.type_map.get(t)
        if handler:
            return handler(something)
        elif isinstance(something, _LLSD):
            return self.type_map[_LLSD](something)
        else:
            try:
                return self.ARRAY(iter(something))
            except TypeError:
                raise LLSDSerializationError(
                    "Cannot serialize unknown type: %s (%s)" % (t, something))

    def format(self, something):
        """
        Format a python object as application/llsd+notation

        :param something: a python object (typically a dict) to be serialized.
        :returns: Returns a LLSD notation formatted string.
        """
        return self._generate(something)


def format_notation(something):
    """
    Format a python object as application/llsd+notation

    :param something: a python object (typically a dict) to be serialized.
    :returns: Returns a LLSD notation formatted string.

    See http://wiki.secondlife.com/wiki/LLSD#Notation_Serialization
    """
    return LLSDNotationFormatter().format(something)


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
