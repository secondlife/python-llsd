import calendar
from collections import deque
import datetime
import io
import struct
import uuid

from llsd.base import (_LLSD, LLSDBaseFormatter, LLSDBaseParser, LLSDSerializationError, BINARY_HEADER,
                       LLSDSerializationError, UnicodeType, _str_to_bytes, binary, is_integer, is_string, uri)


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
    __slots__ = ['_dispatch', '_keep_binary', 'parse_stack']

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
        self.parse_stack = deque([])

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
        "The actual iterative parser."
        cc = self._getc()
        if cc == b'{':
            cur_result = {}
            max_size = struct.unpack("!i", self._getc(4))[0]
        elif cc == b'[':
            cur_result = []
            max_size = struct.unpack("!i", self._getc(4))[0]
        else:
            return self._dispatch[ord(cc)]()
        self.parse_stack.appendleft([0, max_size, cc, cur_result])
        while True:
            item_count, max_size, iter_type, cur_result = self.parse_stack[0]
            cc = self._getc()
            if iter_type == b'{':
                if cc == b'}':
                    item_count, max_size, iter_type, cur_result = self.parse_stack.popleft()
                    if item_count != max_size:
                        self._error("Invalid map close token")
                else:
                    if cc == b'k':
                        key = self._parse_string()
                    elif cc in (b"'", b'"'):
                        key = self._parse_string_delim(cc)
                    else:
                        self._error("invalid map key %d" % ord(cc), -1)
                    cc = self._getc()
                    self.parse_stack[0][0]  = item_count + 1
                    cur_result[key] = self._dispatch[ord(cc)]()
            elif iter_type == b'[':
                if cc == b']':
                    item_count, max_size, iter_type, cur_result = self.parse_stack.popleft()
                    if item_count != max_size:
                        self._error("Invalid array close token")
                else:
                    self.parse_stack[0][0]  = item_count + 1
                    cur_result.append(self._dispatch[ord(cc)]())
            if (len(self.parse_stack) == 0):
                return cur_result

    def _parse_map(self):
        "Parse a single llsd map"
        result = {}
        max_size = struct.unpack("!i", self._getc(4))[0]
        self.parse_stack.appendleft([0, max_size, b'{', result])
        return result

    def _parse_array(self):
        "Parse a single llsd array"
        result = []
        max_size = self._getc(4)
        max_size = struct.unpack("!i", max_size)[0]
        self.parse_stack.appendleft([0, max_size, b'[', result])
        return result

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



class LLSDBinaryFormatter(LLSDBaseFormatter):
    """
    Serialize a python object as application/llsd+binary

    See http://wiki.secondlife.com/wiki/LLSD#Notation_Serialization
    """
    def _LLSD(self, v):
        raise LLSDSerializationError("We should never end up here") # pragma: no cover
    def _UNDEF(self, v):
        self.stream.write(b'!')
    def _BOOLEAN(self, v):
        self.stream.write(b'1' if v else b'0')
    def _INTEGER(self, v):
        try:
            self.stream.writelines([b'i', struct.pack('!i', v)])
        except (OverflowError, struct.error) as exc:
            raise LLSDSerializationError(str(exc), v)
    def _REAL(self, v):
        try:
            self.stream.writelines([b'r', struct.pack('!d', v)])
        except SystemError as exc:
            raise LLSDSerializationError(str(exc), something)
    def _UUID(self, v):
        self.stream.writelines([b'u', v.bytes])
    def _BINARY(self, v):
        self.stream.writelines([b'b', struct.pack('!i', len(v)), v])
    def _STRING(self, v):
        v = _str_to_bytes(v)
        self.stream.writelines([b's', struct.pack('!i', len(v)), v])
    def _URI(self, v):
        uri_bytes = _str_to_bytes(v)
        self.stream.writelines([b'l', struct.pack('!i', len(uri_bytes)), uri_bytes])
    def _DATE(self, v):
        if isinstance(v, datetime.datetime):
            seconds_since_epoch = calendar.timegm(v.utctimetuple()) \
                + v.microsecond // 1e6
        if isinstance(v, datetime.date):
            seconds_since_epoch = calendar.timegm(v.timetuple())
        self.stream.writelines([b'd', struct.pack('<d', seconds_since_epoch)])
    def _ARRAY(self, v):
        self.stream.writelines([b'[', struct.pack('!i', len(v))])
        self.iter_stack.append([iter(v), b"]", None])
    def _MAP(self, v):
        self.stream.writelines([b'{', struct.pack('!i', len(v))])
        self.iter_stack.append([iter(v), b"}", v])

    def _write(self, something):
        """
        Serialize a python object to self.stream as application/llsd+notation.

        :param something: A python object (typically a dict) to be serialized.

        """

        self.stream.write(b'<?llsd/binary?>\n')
        self.iter_stack = [[iter([something]), b"", None]]
        while True:
            cur_iter, iter_type, iterable_obj = self.iter_stack[-1]
            try:
                item = next(cur_iter)
                if iterable_obj:
                    key = _str_to_bytes(item)
                    self.stream.writelines([b'k', struct.pack('!i', len(key)), key])
                    item = iterable_obj[item] # pylint: disable=unsubscriptable-object
                while isinstance(item, _LLSD):
                    item = item.thing
                item_type = type(item)
                if item_type not in self.type_map:
                    raise LLSDSerializationError(
                        "Cannot serialize unknown type: %s (%s)" % (item_type, item))
                self.type_map[item_type](item)
            except StopIteration:
                self.stream.write(iter_type)
                self.iter_stack.pop()
            if len(self.iter_stack) == 1:
                break

def format_binary(something):
    """
    Format application/llsd+binary to a python object.

    See http://wiki.secondlife.com/wiki/LLSD#Binary_Serialization

   :param something: a python object (typically a dict) to be serialized.
   :returns: Returns a LLSD binary formatted string.
    """
    return LLSDBinaryFormatter().format(something)


def write_binary(stream, something):
    return LLSDBinaryFormatter().write(stream, something)


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
