import base64
import binascii
import re
import uuid

from llsd.base import (_LLSD, B, LLSDBaseFormatter, LLSDBaseParser, LLSDParseError, LLSDSerializationError, UnicodeType,
                       _format_datestr, _parse_datestr, _str_to_bytes, binary, uri)

_int_regex = re.compile(br"[-+]?\d+")
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
            # undefined -- have to eat the '!'
            b'!': lambda: self._skip_then(None),
            # false -- have to eat the '0'
            b'0': lambda: self._skip_then(False),
            # true -- have to eat the '1'
            b'1': lambda: self._skip_then(True),
            # false, must check for F|f|false|FALSE
            b'F': lambda: self._get_re("'false'", _false_regex, False),
            b'f': lambda: self._get_re("'false'", _false_regex, False),
            # true, must check for T|t|true|TRUE
            b'T': lambda: self._get_re("'true'", _true_regex, True),
            b't': lambda: self._get_re("'true'", _true_regex, True),
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
        self._dispatch = 256*[lambda: self._error("Invalid notation token")]
        # Then fill in specific entries based on the dict above.
        for c, func in _dispatch_dict.items():
            self._dispatch[ord(c)] = func

    def parse(self, buffer, ignore_binary = False):
        """
        This is the basic public interface for parsing.

        :param buffer: the notation string to parse.
        :param ignore_binary: parser throws away data in llsd binary nodes.
        :returns: returns a python object.
        """
        if buffer == b"":
            return False

        self._buffer = buffer
        self._index = 0
        return self._parse()

    def _get_until(self, delim):
        start = self._index
        end = self._buffer.find(delim, start)
        if end == -1:
            return None
        else:
            self._index = end + 1
            return self._buffer[start:end]

    def _skip_then(self, value):
        # We've already _peek()ed at the current character, which is how we
        # decided to call this method. Skip past it and return constant value.
        self._getc()
        return value

    def _get_re(self, desc, regex, override=None):
        match = re.match(regex, self._buffer[self._index:])
        if not match:
            self._error("Invalid %s token" % desc)
        else:
            self._index += match.end()
            return override if override is not None else match.group(0)

    def _parse(self):
        "The notation parser workhorse."
        cc = self._peek()
        try:
            func = self._dispatch[ord(cc)]
        except IndexError:
            # output error if the token was out of range
            self._error("Invalid notation token")
        else:
            return func()

    def _parse_binary(self):
        "parse a single binary object."

        self._getc()    # eat the beginning 'b'
        cc = self._peek()
        if cc == b'(':
            # parse raw binary
            paren = self._getc()

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
            base = self._getc(2)
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

    def _parse_map(self):
        """
        parse a single map

        map: { string:object, string:object }
        """
        rv = {}
        key = b''
        found_key = False
        self._getc()   # eat the beginning '{'
        cc = self._peek()
        while (cc != b'}'):
            if cc is None:
                self._error("Unclosed map")
            if not found_key:
                if cc in (b"'", b'"', b's'):
                    key = self._parse_string()
                    found_key = True
                elif cc.isspace() or cc == b',':
                    self._getc()    # eat the character
                    pass
                else:
                    self._error("Invalid map key")
            elif cc.isspace():
                self._getc()    # eat the space
                pass
            elif cc == b':':
                self._getc()    # eat the ':'
                value = self._parse()
                rv[key] = value
                found_key = False
            else:
                self._error("missing separator")
            cc = self._peek()

        if self._getc() != b'}':
            self._error("Invalid map close token")

        return rv

    def _parse_array(self):
        """
        parse a single array.

        array: [ object, object, object ]
        """
        rv = []
        self._getc()    # eat the beginning '['
        cc = self._peek()
        while (cc != b']'):
            if cc is None:
                self._error('Unclosed array')
            if cc.isspace() or cc == b',':
                self._getc()
                cc = self._peek()
                continue
            rv.append(self._parse())
            cc = self._peek()

        if self._getc() != b']':
            self._error("Invalid array close token")
        return rv

    def _parse_uuid(self):
        "Parse a uuid."
        self._getc()    # eat the beginning 'u'
        # see comment on LLSDNotationFormatter.UUID() re use of latin-1
        return uuid.UUID(hex=self._getc(36).decode('latin-1'))

    def _parse_uri(self):
        "Parse a URI."
        self._getc()    # eat the beginning 'l'
        return uri(self._parse_string())

    def _parse_date(self):
        "Parse a date."
        self._getc()    # eat the beginning 'd'
        datestr = self._parse_string()
        return _parse_datestr(datestr)

    def _parse_real(self):
        "Parse a floating point number."
        self._getc()    # eat the beginning 'r'
        return float(self._get_re("real", _real_regex))

    def _parse_integer(self):
        "Parse an integer."
        self._getc()    # eat the beginning 'i'
        return int(self._get_re("integer", _int_regex))

    def _parse_string(self):
        """
        Parse a string

        string: "g\'day" | 'have a "nice" day' | s(size)"raw data"
        """
        rv = ""
        delim = self._peek()
        if delim in (b"'", b'"'):
            delim = self._getc()        # eat the beginning delim
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
        self._getc()    # eat the beginning 's'
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


class LLSDNotationFormatter(LLSDBaseFormatter):
    """
    Serialize a python object as application/llsd+notation

    See http://wiki.secondlife.com/wiki/LLSD#Notation_Serialization
    """
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
    return LLSDNotationParser().parse(something)