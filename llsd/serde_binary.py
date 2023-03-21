import calendar
import datetime
import io
import struct
import uuid

from llsd.base import (_LLSD, LLSDBaseParser, LLSDSerializationError, BINARY_HEADER,
                       _str_to_bytes, binary, is_integer, is_string, uri)


try:
    # Python 2: make 'range()' lazy like Python 3
    range = xrange
except NameError:
    # Python 3: 'range()' is already lazy
    pass


class LLSDBinaryParser(LLSDBaseParser):
    """
    Parse application/llsd+binary to a python object.

    See http://wiki.secondlife.com/wiki/LLSD#Binary_Serialization
    """
    __slots__ = ['_dispatch', '_keep_binary']

    def __init__(self):
        super(LLSDBinaryParser, self).__init__()
        # One way of dispatching based on the next character we see would be a
        # dict lookup, and indeed that's the best way to express it in source.
        _dispatch_dict = {
            b'{': self._parse_map,
            b'[': self._parse_array,
            b'!': lambda: None,
            b'0': lambda: False,
            b'1': lambda: True,
            # 'i' = integer
            b'i': lambda: struct.unpack("!i", self._getc(4))[0],
            # 'r' = real number
            b'r': lambda: struct.unpack("!d", self._getc(8))[0],
            # 'u' = uuid
            b'u': lambda: uuid.UUID(bytes=self._getc(16)),
            # 's' = string
            b's': self._parse_string,
            # delimited/escaped string
            b"'": lambda: self._parse_string_delim(b"'"),
            b'"': lambda: self._parse_string_delim(b'"'),
            # 'l' = uri
            b'l': lambda: uri(self._parse_string()),
            # 'd' = date in seconds since epoch
            b'd': self._parse_date,
            # 'b' = binary
            # *NOTE: if not self._keep_binary, maybe have a binary placeholder
            # which has the length.
            b'b': lambda: bytes(self._parse_string_raw()) if self._keep_binary else None,
            }
        # But in fact it should be even faster to construct a list indexed by
        # ord(char). Start by filling it with the 'else' case. Use offset=-1
        # because by the time we perform this lookup, we've scanned past the
        # lookup char.
        self._dispatch = 256*[lambda: self._error("invalid binary token", -1)]
        # Now use the entries in _dispatch_dict to set the corresponding
        # entries in _dispatch.
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
        self._keep_binary = not ignore_binary
        try:
            return self._parse()
        except struct.error as exc:
            self._error(exc)

    def _parse(self):
        "The actual parser which is called recursively when necessary."
        cc = self._getc()
        try:
            func = self._dispatch[ord(cc)]
        except IndexError:
            self._error("invalid binary token", -1)
        else:
            return func()

    def _parse_map(self):
        "Parse a single llsd map"
        rv = {}
        size = struct.unpack("!i", self._getc(4))[0]
        count = 0
        cc = self._getc()
        key = b''
        while (cc != b'}') and (count < size):
            if cc == b'k':
                key = self._parse_string()
            elif cc in (b"'", b'"'):
                key = self._parse_string_delim(cc)
            else:
                self._error("invalid map key", -1)
            value = self._parse()
            rv[key] = value
            count += 1
            cc = self._getc()
        if cc != b'}':
            self._error("invalid map close token")
        return rv

    def _parse_array(self):
        "Parse a single llsd array"
        rv = []
        size = struct.unpack("!i", self._getc(4))[0]
        for count in range(size):
            rv.append(self._parse())
        if self._getc() != b']':
            self._error("invalid array close token")
        return rv

    def _parse_string(self):
        try:
            return self._parse_string_raw().decode('utf-8')
        except UnicodeDecodeError as exc:
            self._error(exc)

    def _parse_string_raw(self):
        "Parse a string which has the leadings size indicator"
        try:
            size = struct.unpack("!i", self._getc(4))[0]
        except struct.error as exc:
            # convert exception class for client convenience
            self._error("struct " + str(exc))
        rv = self._getc(size)
        return rv

    def _parse_date(self):
        seconds = struct.unpack("<d", self._getc(8))[0]
        try:
            return datetime.datetime.utcfromtimestamp(seconds)
        except (OSError, OverflowError) as exc:
            # A garbage seconds value can cause utcfromtimestamp() to raise
            # OverflowError: timestamp out of range for platform time_t
            self._error(exc, -8)


def format_binary(something):
    """
    Format application/llsd+binary to a python object.

    See http://wiki.secondlife.com/wiki/LLSD#Binary_Serialization

   :param something: a python object (typically a dict) to be serialized.
   :returns: Returns a LLSD binary formatted string.
    """
    stream = io.BytesIO()
    write_binary(stream, something)
    return stream.getvalue()


def write_binary(stream, something):
    stream.write(b'<?llsd/binary?>\n')
    _write_binary_recurse(stream, something)


def _write_binary_recurse(stream, something):
    "Binary formatter workhorse."
    if something is None:
        stream.write(b'!')
    elif isinstance(something, _LLSD):
        _write_binary_recurse(stream, something.thing)
    elif isinstance(something, bool):
        stream.write(b'1' if something else b'0')
    elif is_integer(something):
        try:
            stream.writelines([b'i', struct.pack('!i', something)])
        except (OverflowError, struct.error) as exc:
            raise LLSDSerializationError(str(exc), something)
    elif isinstance(something, float):
        try:
            stream.writelines([b'r', struct.pack('!d', something)])
        except SystemError as exc:
            raise LLSDSerializationError(str(exc), something)
    elif isinstance(something, uuid.UUID):
        stream.writelines([b'u', something.bytes])
    elif isinstance(something, binary):
        stream.writelines([b'b', struct.pack('!i', len(something)), something])
    elif is_string(something):
        something = _str_to_bytes(something)
        stream.writelines([b's', struct.pack('!i', len(something)), something])
    elif isinstance(something, uri):
        stream.writelines([b'l', struct.pack('!i', len(something)), something])
    elif isinstance(something, datetime.datetime):
        seconds_since_epoch = calendar.timegm(something.utctimetuple()) \
                              + something.microsecond // 1e6
        stream.writelines([b'd', struct.pack('<d', seconds_since_epoch)])
    elif isinstance(something, datetime.date):
        seconds_since_epoch = calendar.timegm(something.timetuple())
        stream.writelines([b'd', struct.pack('<d', seconds_since_epoch)])
    elif isinstance(something, (list, tuple)):
        _write_list(stream, something)
    elif isinstance(something, dict):
        stream.writelines([b'{', struct.pack('!i', len(something))])
        for key, value in something.items():
            key = _str_to_bytes(key)
            stream.writelines([b'k', struct.pack('!i', len(key)), key])
            _write_binary_recurse(stream, value)
        stream.write(b'}')
    else:
        try:
            return _write_list(stream, list(something))
        except TypeError:
            raise LLSDSerializationError(
                "Cannot serialize unknown type: %s (%s)" %
                (type(something), something))


def _write_list(stream, something):
    stream.writelines([b'[', struct.pack('!i', len(something))])
    for item in something:
        _write_binary_recurse(stream, item)
    stream.write(b']')


def parse_binary(something):
    """
    This is the basic public interface for parsing llsd+binary.

    :param something: The data to parse in an indexable sequence.
    :returns: Returns a python object.
    """
    # Try to match header, and if matched, skip past it.
    parser = LLSDBaseParser(something)
    parser.matchseq(BINARY_HEADER)
    # If we matched the header, then parse whatever follows, else parse the
    # original bytes object or stream.
    return parse_binary_nohdr(parser)


def parse_binary_nohdr(baseparser):
    """
    Parse llsd+binary known to be without a header.

    :param baseparser: LLSDBaseParser instance wrapping the data to parse.
    :returns: Returns a python object.
    """
    return LLSDBinaryParser().parse(baseparser)
