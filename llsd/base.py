import abc
import base64
import binascii
import datetime
import io
import os
import re
import sys
import types
import uuid

try:
    # If the future package is installed, then we support it.  Any clients in
    # python 2 using its str builtin replacement will actually be using instances
    # of newstr, so we need to properly detect that as a string type
    # for details see the docs: http://python-future.org/str_object.html
    from future.types.newstr import newstr
except ImportError:
    # otherwise we pass over it in silence
    newstr = str

PY2 = sys.version_info[0] == 2

XML_MIME_TYPE = 'application/llsd+xml'
BINARY_MIME_TYPE = 'application/llsd+binary'
NOTATION_MIME_TYPE = 'application/llsd+notation'

ALL_CHARS = str(bytearray(range(256))) if PY2 else bytes(range(256))


class _LLSD:
    __metaclass__ = abc.ABCMeta

    def __init__(self, thing=None):
        self.thing = thing


undef = _LLSD(None)


if PY2:
    class binary(str):
        "Simple wrapper for llsd.binary data."
        pass
else:
    binary = bytes


class uri(str):
    "Simple wrapper for llsd.uri data."
    pass


class LLSDParseError(Exception):
    "Exception raised when the parser fails."
    pass


class LLSDSerializationError(TypeError):
    "Exception raised when serialization fails."
    pass


# In Python 2, this expression produces (str, unicode); in Python 3 it's
# simply (str,). Either way, it's valid to test isinstance(somevar,
# StringTypes). (Some consumers test (type(somevar) in StringTypes), so we do
# want (str,) rather than plain str.)
StringTypes = tuple(set((type(''), type(u''), newstr)))

try:
    LongType = long
    IntTypes = (int, long)
except NameError:
    LongType = int
    IntTypes = int

try:
    UnicodeType = unicode
except NameError:
    UnicodeType = str

try:
    b'%s' % (b'yes',)
except TypeError:
    # There's a range of Python 3 versions, up through Python 3.4, for which
    # bytes interpolation (bytes value with % operator) does not work. This
    # hack can be removed once we no longer care about Python 3.4 -- in other
    # words, once we're beyond jessie everywhere.
    class B(object):
        """
        Instead of writing:
        b'format string' % stuff
        write:
        B('format string') % stuff
        This class performs the conversions necessary to support bytes
        interpolation when the language doesn't natively support it.
        (We considered naming this class b, but that would be too confusing.)
        """
        def __init__(self, fmt):
            # Instead of storing the format string as bytes and converting it
            # to string every time, convert initially and store the string.
            try:
                self.strfmt = fmt.decode('utf-8')
            except AttributeError:
                # caller passed a string literal rather than a bytes literal
                self.strfmt = fmt

        def __mod__(self, args):
            # __mod__() is engaged for (self % args)
            if not isinstance(args, tuple):
                # Unify the tuple and non-tuple cases.
                args = (args,)
            # In principle, this is simple: convert everything to string,
            # interpolate, convert back. It's complicated by the fact that we
            # must handle non-bytes args.
            strargs = []
            for arg in args:
                try:
                    decoder = arg.decode
                except AttributeError:
                    # use arg exactly as is
                    strargs.append(arg)
                else:
                    # convert from bytes to string
                    strargs.append(decoder('utf-8'))
            return (self.strfmt % tuple(strargs)).encode('utf-8')
else:
    # bytes interpolation Just Works
    def B(fmt):
        try:
            # In the usual case, caller wrote B('fmt') rather than b'fmt'. But
            # s/he really wants a bytes literal here. Encode the passed string.
            return fmt.encode('utf-8')
        except AttributeError:
            # Caller wrote B(b'fmt')?
            return fmt


class PY3SemanticBytes(bytes):
    """Wrapper to make `buffer[n]` return an integer like in Py3"""
    __slots__ = []

    def __getitem__(self, item):
        ret = super(PY3SemanticBytes, self).__getitem__(item)
        # `buffer[n]` should return an integer, but slice syntax like
        # `buffer[n:n+1]` should still return a `Bytes` object as before.
        if is_integer(item):
            return ord(ret)
        return ret


def is_integer(o):
    """ portable test if an object is like an int """
    return isinstance(o, IntTypes)


def is_unicode(o):
    """ portable check if an object is unicode and not bytes """
    return isinstance(o, UnicodeType)


def is_string(o):
    """ portable check if an object is string-like """
    return isinstance(o, StringTypes)


def is_bytes(o):
    """ portable check if an object is an immutable byte array """
    return isinstance(o, bytes)


#date: d"YYYY-MM-DDTHH:MM:SS.FFFFFFZ"
_date_regex = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T"
                        r"(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})"
                        r"(?P<second_float>(\.\d+)?)Z")


def _str_to_bytes(s):
    if is_unicode(s):
        return s.encode('utf-8')
    else:
        return s


def _format_datestr(v):
    """
    Formats a datetime or date object into the string format shared by
    xml and notation serializations.
    """
    if not isinstance(v, datetime.date) and not isinstance(v, datetime.datetime):
        raise LLSDParseError("invalid date string %s passed to date formatter" % v)

    if not isinstance(v, datetime.datetime):
        v = datetime.datetime.combine(v, datetime.time(0))

    return _str_to_bytes(v.isoformat() + 'Z')


def _parse_datestr(datestr):
    """
    Parses a datetime object from the string format shared by
    xml and notation serializations.
    """
    if datestr == "":
        return datetime.datetime(1970, 1, 1)

    match = re.match(_date_regex, datestr)
    if not match:
        raise LLSDParseError("invalid date string '%s'." % datestr)

    year = int(match.group('year'))
    month = int(match.group('month'))
    day = int(match.group('day'))
    hour = int(match.group('hour'))
    minute = int(match.group('minute'))
    second = int(match.group('second'))
    seconds_float = match.group('second_float')
    usec = 0
    if seconds_float:
        usec = int(float('0' + seconds_float) * 1e6)
    return datetime.datetime(year, month, day, hour, minute, second, usec)


def _bool_to_python(node):
    "Convert boolean node to a python object."
    val = node.text or ''
    try:
        # string value, accept 'true' or 'True' or whatever
        return (val.lower() in ('true', '1', '1.0'))
    except AttributeError:
       # not a string (no lower() method), use normal Python rules
       return bool(val)


def _int_to_python(node):
    "Convert integer node to a python object."
    val = node.text or ''
    if not val.strip():
        return 0
    return int(val)


def _real_to_python(node):
    "Convert floating point node to a python object."
    val = node.text or ''
    if not val.strip():
        return 0.0
    return float(val)


def _uuid_to_python(node):
    "Convert uuid node to a python object."
    if node.text:
        return uuid.UUID(hex=node.text)
    return uuid.UUID(int=0)


def _str_to_python(node):
    "Convert string node to a python object."
    return node.text or ''


def _bin_to_python(node):
    base = node.get('encoding') or 'base64'
    try:
        if base == 'base16':
            # parse base16 encoded data
            return binary(base64.b16decode(node.text or ''))
        elif base == 'base64':
            # parse base64 encoded data
            return binary(base64.b64decode(node.text or ''))
        elif base == 'base85':
            return LLSDParseError("Parser doesn't support base85 encoding")
    except binascii.Error as exc:
        # convert exception class so it's more catchable
        return LLSDParseError("Encoded binary data: " + str(exc))
    except TypeError as exc:
        # convert exception class so it's more catchable
        return LLSDParseError("Bad binary data: " + str(exc))


def _date_to_python(node):
    "Convert date node to a python object."
    val = node.text or ''
    if not val:
        val = "1970-01-01T00:00:00Z"
    return _parse_datestr(val)


def _uri_to_python(node):
    "Convert uri node to a python object."
    val = node.text or ''
    return uri(val)


def _map_to_python(node):
    "Convert map node to a python object."
    result = {}
    for index in range(len(node))[::2]:
        if node[index].text is None:
            result[''] = _to_python(node[index+1])
        else:
            result[node[index].text] = _to_python(node[index+1])
    return result


def _array_to_python(node):
    "Convert array node to a python object."
    return [_to_python(child) for child in node]


NODE_HANDLERS = dict(
    undef=lambda x: None,
    boolean=_bool_to_python,
    integer=_int_to_python,
    real=_real_to_python,
    uuid=_uuid_to_python,
    string=_str_to_python,
    binary=_bin_to_python,
    date=_date_to_python,
    uri=_uri_to_python,
    map=_map_to_python,
    array=_array_to_python,
)


def _to_python(node):
    "Convert node to a python object."
    return NODE_HANDLERS[node.tag](node)


class LLSDBaseFormatter(object):
    """
    This base class cannot be instantiated on its own: it assumes a subclass
    containing methods with canonical names specified in self.__init__(). The
    role of this base class is to provide self.type_map based on the methods
    defined in its subclass.
    """
    def __init__(self):
        "Construct a new formatter dispatch table."
        self.type_map = {
            type(None):          self.UNDEF,
            undef:               self.UNDEF,
            bool:                self.BOOLEAN,
            int:                 self.INTEGER,
            LongType:            self.INTEGER,
            float:               self.REAL,
            uuid.UUID:           self.UUID,
            binary:              self.BINARY,
            str:                 self.STRING,
            UnicodeType:         self.STRING,
            newstr:              self.STRING,
            uri:                 self.URI,
            datetime.datetime:   self.DATE,
            datetime.date:       self.DATE,
            list:                self.ARRAY,
            tuple:               self.ARRAY,
            types.GeneratorType: self.ARRAY,
            dict:                self.MAP,
            _LLSD:               self.LLSD,
        }


_X_ORD = ord(b'x')
_BACKSLASH_ORD = ord(b'\\')
_DECODE_BUFF_ALLOC_SIZE = 1024


class LLSDBaseParser(object):
    """
    Utility methods useful for parser subclasses.
    """
    __slots__ = ['_util', '_decode_buff']

    def __init__(self):
        self._util = BytesUtil(b'')
        # Scratch space for decoding delimited strings
        self._decode_buff = bytearray(_DECODE_BUFF_ALLOC_SIZE)

    def _reset(self, something):
        if isinstance(something, bytes):
            self._util = BytesUtil(something)
        elif hasattr(something, 'seek'):
            self._util = StreamUtil(something)
        else:
            raise LLSDParseError('Input must either be a bytes object '
                                 'or a seekable binary stream')

    def _error(self, message, offset=0):
        self._util.error(message, offset)

    def _peek(self, num=1, full=True):
        # full=True means error if we can't peek ahead num bytes
        if num < 0:
            # There aren't many ways this can happen. The likeliest is that
            # we've just read garbage length bytes from a binary input string.
            # We happen to know that lengths are encoded as 4 bytes, so back
            # off by 4 bytes to try to point the user at the right spot.
            self._error("Invalid length field %d" % num, -4)
        return self._util.peek(num, full)

    def _getc(self, num=1, full=True):
        # full=True means error if we can't peek ahead num bytes
        return self._util.getc(num, full)

    # map char following escape char to corresponding character
    _escaped = {
        ord(b'a'): ord(b'\a'),
        ord(b'b'): ord(b'\b'),
        ord(b'f'): ord(b'\f'),
        ord(b'n'): ord(b'\n'),
        ord(b'r'): ord(b'\r'),
        ord(b't'): ord(b'\t'),
        ord(b'v'): ord(b'\v'),
    }

    def _parse_string_delim(self, delim):
        "Parse a delimited string."
        insert_idx = 0
        delim_ord = ord(delim)
        # Preallocate a working buffer for the decoded string output
        # to avoid allocs in the hot loop.
        decode_buff = self._decode_buff
        # Cache this in locals, otherwise we have to perform a lookup on
        # `self` in the hot loop.
        util = self._util
        cc = 0
        while True:
            try:
                cc = ord(util.getc())

                if cc == _BACKSLASH_ORD:
                    # Backslash, figure out if this is an \xNN hex escape or
                    # something like \t
                    cc = ord(util.getc())
                    if cc == _X_ORD:
                        # It's a hex escape. char is the value of the two
                        # following hex nybbles. This slice may result in
                        # a short read (0 or 1 bytes), but either a
                        # `ValueError` will be triggered by the first case,
                        # and the second will cause an `IndexError` on the
                        # next iteration of the loop.
                        hex_bytes = util.getc(2)
                        try:
                            # int() can parse a `bytes` containing hex,
                            # no explicit `bytes.decode("ascii")` required.
                            cc = int(hex_bytes, 16)
                        except ValueError as e:
                            # One of the hex characters was likely invalid.
                            # Wrap the ValueError so that we can provide a
                            # byte offset in the error.
                            self._error(e, offset=-2)
                    else:
                        # escape char preceding anything other than the chars
                        # in _escaped just results in that same char without
                        # the escape char
                        cc = self._escaped.get(cc, cc)
                elif cc == delim_ord:
                    break
            except IndexError:
                # We can be reasonably sure that any IndexErrors inside here
                # were caused by an out-of-bounds `buff[read_idx]`.
                self._error("Trying to read past end of buffer")

            try:
                decode_buff[insert_idx] = cc
            except IndexError:
                # Oops, that overflowed the decoding buffer, make a
                # new expanded buffer containing the existing contents.
                decode_buff = bytearray(decode_buff)
                decode_buff.extend(b"\x00" * _DECODE_BUFF_ALLOC_SIZE)
                decode_buff[insert_idx] = cc

            insert_idx += 1

        # Sync our local read index with the canonical one
        try:
            # Slice off only what we used of the working decode buffer
            return decode_buff[:insert_idx].decode('utf-8')
        except UnicodeDecodeError as exc:
            self._error(exc)


class BytesUtil:
    """
    Utility methods implemented on an input bytes object
    """
    __slots__ = ['_buffer', '_index']

    def __init__(self, input):
        self._buffer = input
        self._index = 0

    def error(self, message, offset=0):
        try:
            byte = chr(self._buffer[self._index+offset])
        except IndexError:
            byte = None
        raise LLSDParseError("%s at byte %d: %r" % (message, self._index+offset, byte))

    def peek(self, num, full=True):
        if full and self._index + num > len(self._buffer):
            self.error("Trying to read past end of buffer")
        return self._buffer[self._index:self._index + num]

    def getc(self, num=1, full=True):
        chars = self.peek(num, full)
        self._index += num
        return chars


class StreamUtil:
    """
    Utility methods implemented on an input bytes stream
    """
    __slots__ = ['_stream']

    def __init__(self, stream):
        self._stream = stream

    def error(self, message, offset=0):
        oldpos = self._stream.tell()
        self._stream.seek(offset)
        raise LLSDParseError("%s at byte %d: %r" % (message, oldpos+offset,
                                                    self._peek(1, full=False)))

    def peek(self, num, full=True):
        oldpos = self._stream.tell()
        try:
            return self.getc(num, full)
        finally:
            self._stream.seek(oldpos)

    def getc(self, num=1, full=True):
        got = self._stream.read(num)
        if full and len(got) < num:
            self.error("Trying to read past end of stream")
        return got


def matchseq(something, pattern):
    """
    Given a 'something' that's either a bytes object or a seekable binary
    stream, match bytes object 'pattern' after skipping arbitrary leading
    whitespace. After successfully matching 'pattern', skip trailing
    whitespace as well.

    'pattern' is NOT a regular expression, but a bytes string in which each
    space character represents zero or more whitespace characters. Non-space
    characters are matched case-insensitively.

    If 'pattern' matches, return 'something' advanced to skip what was
    matched: for a bytes object, a subrange; for a binary stream, that stream
    advanced past the last byte examined.

    If 'pattern' does not match, return None and reset the binary stream to
    its original read position.
    """
    return _matchseq(MatchStream.for_(something), pattern)


def starts_with(startstr, something):
    """
    Like matchseq(), except that starts_with() doesn't consume what it
    matches: it always resets 'something' to initial position, returning True
    or False depending on whether the 
    """
    stream = MatchStream.for_(something)
    match = _matchseq(stream, startstr)
    stream.reset()
    return bool(match)


class MatchStream:
    """
    Common operations for BytesStream and AnyStream
    """
    @staticmethod
    def for_(something):
        # We want to treat a bytes object and a stream uniformly
        return BytesStream(something) if isinstance(something, bytes) else AnyStream(something)

    def next_nonblank(self):
        c = self.read(1)
        while c.isspace():
            c = self.read(1)
        return c


class BytesStream(io.BytesIO, MatchStream):
    """
    Wrapper for a bytes object passed to matchseq() to treat as a stream.
    """
    def reset(self, offset=0, whence=io.SEEK_SET):
        # Since matchseq() constructs this BytesStream object, we know its
        # initial read pointer is 0.
        self.seek(offset, whence)

    def remainder(self):
        # return a subset of the caller's original bytes object,
        # skipping what we've already read
        return self.getvalue()[self.tell():]


class AnyStream(MatchStream):
    """
    Wrapper for a stream passed to matchseq() with specific supplemental
    methods.
    """
    def __init__(self, stream):
        self.stream = stream
        self.initpos = self.stream.tell()

    def read(self, size):
        return self.stream.read(size)

    def reset(self, offset=None, whence=io.SEEK_SET):
        self.stream.seek(self.initpos if offset is None else offset, whence)

    def remainder(self):
        # return caller's original stream object, with read position advanced
        return self.stream


def _matchseq(stream, pattern):
    """
    Given a MatchStream subclass instance 'stream', match bytes object
    'pattern' after skipping arbitrary leading whitespace. After successfully
    matching 'pattern', skip trailing whitespace as well.

    'pattern' is NOT a regular expression, but a bytes string in which each
    space character represents zero or more whitespace characters. Non-space
    characters are matched case-insensitively.

    If 'pattern' matches, return 'stream' advanced to skip what was matched:
    for BytesStream, a subrange; for AnyStream, that stream advanced past the
    last byte examined.

    If 'pattern' does not match, return None and reset the AnyStream to its
    original read position.
    """
    for chunk in pattern.split():
        # skip leading space before this chunk
        c = stream.next_nonblank()
        # if we hit EOF, no match
        if not c:
            stream.reset()
            return None
        # not EOF: try to match non-empty chunk,
        # not forgetting that 'c' is a lookahead byte
        # (split() never produces a zero-length chunk)
        maybe = c + stream.read(len(chunk)-1)
        if maybe.lower() != chunk.lower():
            # mismatch, reset
            stream.reset()
            return None
        # so far so good, back for next chunk

    # here we've matched every chunk, with the read pointer just at the end of
    # the last matched chunk -- skip trailing space
    if stream.next_nonblank():
        # back up one character, i.e. put back the nonblank
        stream.reset(-1, io.SEEK_CUR)
    # show caller where we ended up
    return stream.remainder()
