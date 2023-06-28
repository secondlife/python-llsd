import base64
import binascii
from collections import deque
import io
import re
import uuid

from llsd.base import (_LLSD, ALL_CHARS, LLSDBaseParser, LLSDBaseFormatter, XML_HEADER,
                       LLSDParseError, LLSDSerializationError, UnicodeType,
                       _format_datestr, _str_to_bytes, is_unicode, PY2, uri, binary, _parse_datestr)
from llsd.fastest_elementtree import ElementTreeError, fromstring, parse as _parse

INVALID_XML_BYTES = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c'\
                    b'\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18'\
                    b'\x19\x1a\x1b\x1c\x1d\x1e\x1f'
INVALID_XML_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')


XML_ESC_TRANS = {}
if not PY2:
    XML_ESC_TRANS = str.maketrans({'&': '&amp;',
                                   '<':'&lt;',
                                   '>':'&gt;',
                                   u'\uffff':None,   # cannot be parsed
                                   u'\ufffe':None})  # cannot be parsed

    for x in INVALID_XML_BYTES:
        XML_ESC_TRANS[x] = None


def remove_invalid_xml_bytes(b):
    """
    Remove characters that aren't allowed in xml.
    """
    try:
        # Dropping chars that cannot be parsed later on.  The
        # translate() function was benchmarked to be the fastest way
        # to do this.
        return b.translate(ALL_CHARS, INVALID_XML_BYTES)
    except TypeError:
        # we get here if s is a unicode object (should be limited to
        # unit tests)
        return INVALID_XML_RE.sub('', b)

# only python2, which is not covered by coverage tests
def xml_esc(v): # pragma: no cover
    "Escape string or unicode object v for xml output"

    # Use is_unicode() instead of is_string() because in python 2, str is
    # bytes, not unicode, and should not be "encode()"d. Attempts to
    # encode("utf-8") a bytes type will result in an implicit
    # decode("ascii") that will throw a UnicodeDecodeError if the string
    # contains non-ascii characters.
    if is_unicode(v):
        # we need to drop these invalid characters because they
        # cannot be parsed (and encode() doesn't drop them for us)
        v = v.replace(u'\uffff', u'')
        v = v.replace(u'\ufffe', u'')
        v = v.encode('utf-8')
    v = remove_invalid_xml_bytes(v)
    return v.replace(b'&',b'&amp;').replace(b'<',b'&lt;').replace(b'>',b'&gt;')


class LLSDXMLFormatter(LLSDBaseFormatter):
    """
    Class which implements LLSD XML serialization.

    http://wiki.secondlife.com/wiki/LLSD#XML_Serialization

    This class serializes a limited subset of python objects as
    application/llsd+xml. You do not generally need to make an instance of
    this class since the module level format_xml() is the most convenient
    interface to this functionality.
    """

    def __init__(self, indent_atom = None):
        "Construct a serializer."
        # Call the super class constructor so that we have the type map
        super(LLSDXMLFormatter, self).__init__()
        self._indent_atom = b''
        self._eol = b''
        self._indent_level = 0

    def _indent(self):
        pass

    def _LLSD(self, v):
        return self._generate(v.thing)
    def _UNDEF(self, _v):
        self.stream.writelines([b'<undef/>', self._eol])
    def _BOOLEAN(self, v):
        if v:
            return self.stream.writelines([b'<boolean>true</boolean>', self._eol])
        self.stream.writelines([b'<boolean>false</boolean>', self._eol])
    def _INTEGER(self, v):
        self.stream.writelines([b'<integer>', str(v).encode('utf-8'), b'</integer>', self._eol])
    def _REAL(self, v):
        self.stream.writelines([b'<real>', str(v).encode('utf-8'),  b'</real>', self._eol])
    def _UUID(self, v):
        if v.int == 0:
            return self.stream.writelines([b'<uuid/>', self._eol])
        self.stream.writelines([b'<uuid>', str(v).encode('utf-8'), b'</uuid>', self._eol])
    def _BINARY(self, v):
        self.stream.writelines([b'<binary>', base64.b64encode(v).strip(), b'</binary>', self._eol])
    def _STRING(self, v):
        # We don't simply have a function that encapsulates the PY2 vs PY3 calls,
        # as that results in another function call and is slightly less performant
        if PY2:    # pragma: no cover
            return self.stream.writelines([b'<string>', _str_to_bytes(xml_esc(v)), b'</string>', self._eol])
        self.stream.writelines([b'<string>', v.translate(XML_ESC_TRANS).encode('utf-8'), b'</string>', self._eol])
    def _URI(self, v):
        # We don't simply have a function that encapsulates the PY2 vs PY3 calls,
        # as that results in another function call and is slightly less performant
        if PY2:    # pragma: no cover
            return self.stream.writelines([b'<uri>', _str_to_bytes(xml_esc(v)), b'</uri>', self._eol])
        self.stream.writelines([b'<uri>', str(v).translate(XML_ESC_TRANS).encode('utf-8'), b'</uri>', self._eol])
    def _DATE(self, v):
        self.stream.writelines([b'<date>', _format_datestr(v), b'</date>', self._eol])
    def _ARRAY(self, v):
        self.stream.writelines([b'<array>', self._eol])
        self._indent_level = self._indent_level + 1
        for item in v:
            self._indent()
            self._generate(item)
        self._indent_level = self._indent_level - 1
        self.stream.writelines([b'</array>', self._eol])
    def _MAP(self, v):
        self.stream.writelines([b'<map>', self._eol])
        self._indent_level = self._indent_level + 1
        for key, value in v.items():
            self._indent()
            if PY2:     # pragma: no cover
                self.stream.writelines([b'<key>',
                                        xml_esc(UnicodeType(key)),
                                        b'</key>',
                                        self._eol])
            else:
                self.stream.writelines([b'<key>',
                                        UnicodeType(key).translate(XML_ESC_TRANS).encode('utf-8'),
                                        b'</key>',
                                        self._eol])
            self._indent()
            self._generate(value)
        self._indent_level = self._indent_level - 1
        self._indent()
        self.stream.writelines([b'</map>', self._eol])

    def _generate(self, something):
        "Generate xml from a single python object."
        t = type(something)
        if t in self.type_map:
            return self.type_map[t](something)
        elif isinstance(something, _LLSD):
            return self.type_map[_LLSD](something)
        else:
            raise LLSDSerializationError(
                "Cannot serialize unknown type: %s (%s)" % (t, something))

    def _write(self, something):
        """
        Serialize a python object to self.stream as application/llsd+xml.
        :param something: A python object (typically a dict) to be serialized.
        """
        self.stream.writelines([b'<?xml version="1.0" ?>', self._eol,
                                b'<llsd>', self._eol])
        self._generate(something)
        self.stream.write(b'</llsd>')


class LLSDXMLPrettyFormatter(LLSDXMLFormatter):
    """
    Class which implements 'pretty' LLSD XML serialization..

    See http://wiki.secondlife.com/wiki/LLSD#XML_Serialization

    The output conforms to the LLSD DTD, unlike the output from the
    standard python xml.dom DOM::toprettyxml() method which does not
    preserve significant whitespace.

    This class is not necessarily suited for serializing very large objects.
    It sorts on dict (llsd map) keys alphabetically to ease human reading.
    """
    def __init__(self, indent_atom = None):
        "Construct a pretty serializer."
        # Call the super class constructor so that we have the type map
        super(LLSDXMLPrettyFormatter, self).__init__()

        # Private data used for indentation.
        self._indent_level = 1
        if indent_atom is None:
            self._indent_atom = b'  '
        else:
            self._indent_atom = indent_atom
        self._eol = b'\n'

    def _indent(self):
        "Write an indentation based on the atom and indentation level."
        self.stream.writelines([self._indent_atom] * self._indent_level)


def format_pretty_xml(something):
    """
    Serialize a python object as 'pretty' application/llsd+xml.

    :param something: a python object (typically a dict) to be serialized.
    :returns: Returns an XML formatted string.

    See http://wiki.secondlife.com/wiki/LLSD#XML_Serialization

    The output conforms to the LLSD DTD, unlike the output from the
    standard python xml.dom DOM::toprettyxml() method which does not
    preserve significant whitespace.
    This function is not necessarily suited for serializing very large
    objects. It sorts on dict (llsd map) keys alphabetically to ease human
    reading.
    """
    return LLSDXMLPrettyFormatter().format(something)


def write_pretty_xml(stream, something):
    """
    Serialize to passed 'stream' the python object 'something' as 'pretty'
    application/llsd+xml.

    :param stream: a binary stream open for writing.
    :param something: a python object (typically a dict) to be serialized.

    See http://wiki.secondlife.com/wiki/LLSD#XML_Serialization

    The output conforms to the LLSD DTD, unlike the output from the
    standard python xml.dom DOM::toprettyxml() method which does not
    preserve significant whitespace.
    This function is not necessarily suited for serializing very large
    objects. It sorts on dict (llsd map) keys alphabetically to ease human
    reading.
    """
    return LLSDXMLPrettyFormatter().write(stream, something)


class LLSDXMLParser:
    def __init__(self):
        "Construct an xml node parser."

        self.NODE_HANDLERS = {
            "undef": lambda x: None,
            "boolean": self._bool_to_python,
            "integer": self._int_to_python,
            "real": self._real_to_python,
            "uuid": self._uuid_to_python,
            "string": self._str_to_python,
            "binary": self._bin_to_python,
            "date": self._date_to_python,
            "uri": self._uri_to_python,
            "map": self._map_to_python,
            "array": self._array_to_python,
        }

        self.parse_stack = deque([])

    def _bool_to_python(self, node):
        "Convert boolean node to a python object."
        val = node.text or ''
        try:
            # string value, accept 'true' or 'True' or whatever
            return (val.lower() in ('true', '1', '1.0'))
        except AttributeError:
            # not a string (no lower() method), use normal Python rules
            return bool(val)

    def _int_to_python(self, node):
        "Convert integer node to a python object."
        val = node.text or ''
        if not val.strip():
            return 0
        return int(val)

    def _real_to_python(self, node):
        "Convert floating point node to a python object."
        val = node.text or ''
        if not val.strip():
            return 0.0
        return float(val)

    def _uuid_to_python(self, node):
        "Convert uuid node to a python object."
        if node.text:
            return uuid.UUID(hex=node.text)
        return uuid.UUID(int=0)

    def _str_to_python(self, node):
        "Convert string node to a python object."
        return node.text or ''

    def _bin_to_python(self, node):
        base = node.get('encoding') or 'base64'
        try:
            if base == 'base16':
                # parse base16 encoded data
                return binary(base64.b16decode(node.text or ''))
            if base == 'base64':
                # parse base64 encoded data
                return binary(base64.b64decode(node.text or ''))
            raise LLSDParseError("Parser doesn't support %s encoding" % base)

        except binascii.Error as exc:
            # convert exception class so it's more catchable
            raise LLSDParseError("Encoded binary data: " + str(exc))
        except TypeError as exc:
            # convert exception class so it's more catchable
            raise LLSDParseError("Bad binary data: " + str(exc))

    def _date_to_python(self, node):
        "Convert date node to a python object."
        val = node.text or ''
        if not val:
            val = "1970-01-01T00:00:00Z"
        return _parse_datestr(val)

    def _uri_to_python(self, node):
        "Convert uri node to a python object."
        val = node.text or ''
        return uri(val)

    def _map_to_python(self, node):
        "Convert map node to a python object."
        new_result = {}
        new_stack_entry = [iter(node), node, new_result]
        self.parse_stack.appendleft(new_stack_entry)
        return new_result

    def _array_to_python(self, node):
        "Convert array node to a python object."
        new_result = []
        new_stack_entry = [iter(node), node, new_result]
        self.parse_stack.appendleft(new_stack_entry)
        return new_result

    def parse_node(self, something):
        """
        Parse an ElementTree tree
        This parser is iterative instead of recursive. It uses
        Each element in parse_stack is an iterator into either the list
        or the dict in the tree. This limits depth by size of free memory 
        instead of size of the function call stack, allowing us to render
        deeper trees than a recursive model.
        :param something: The xml node to parse.
        :returns: Returns a python object.
        """

        # if the passed in element is not a map or array, simply return
        # its value.  Otherwise, create a dict or array to receive
        # child/leaf elements.
        if something.tag == "map":
            cur_result = {}
        elif something.tag == "array":
            cur_result = []
        else:
            if something.tag not in self.NODE_HANDLERS:
                raise LLSDParseError("Unknown value type %s" % something.tag)
            return self.NODE_HANDLERS[something.tag](something)

        # start by pushing the current element iterator data onto
        # the stack
        # 0 - iterator indicating the current position in the given level of the tree
        #     this can be either a list iterator position, or an iterator of
        #     keys for the dict.
        # 1 - the actual element object.
        # 2 - the result for this level in the tree, onto which
        #     children or leafs will be appended/set
        self.parse_stack.appendleft([iter(something), something, cur_result])
        while True:
            node_iter, iterable, cur_result = self.parse_stack[0]
            try:
                value = next(node_iter)

            except StopIteration:
                node_iter, iterable, cur_result = self.parse_stack.popleft()
                if len(self.parse_stack) == 0:
                    break
            else:
                if iterable.tag == "map":
                    if value.tag != "key":
                        raise LLSDParseError("Expected 'key', got %s" % value.tag)
                    key = value.text
                    if key is None:
                        key = ''
                    try:
                        value = next(node_iter)
                    except StopIteration:
                        raise LLSDParseError("No value for map item %s" % key)
                    try:
                        cur_result[key] = self.NODE_HANDLERS[value.tag](value)
                    except KeyError as err:
                        raise LLSDParseError("Unknown value type: " + str(err))
                elif iterable.tag == "array":
                    try:
                        cur_result.append(self.NODE_HANDLERS[value.tag](value))
                    except KeyError as err:
                        raise LLSDParseError("Unknown value type: " + str(err))
        return cur_result

def parse_xml(something):
    """
    This is the basic public interface for parsing llsd+xml.

    :param something: The data to parse.
    :returns: Returns a python object.
    """
    # Try to match header, and if matched, skip past it.
    parser = LLSDBaseParser(something)
    parser.matchseq(XML_HEADER)
    # If we matched the header, then parse whatever follows, else parse the
    # original bytes object or stream.
    return parse_xml_nohdr(parser)




def parse_xml_nohdr(baseparser):
    """
    Parse llsd+xml known to be without an <? LLSD/XML ?> header. May still
    have a normal XML declaration, e.g. <?xml version="1.0" ?>.

    :param baseparser: LLSDBaseParser instance wrapping the data to parse.
    :returns: Returns a python object.
    """
    # Python 3.9's xml.etree.ElementTree.fromstring() does not like whitespace
    # before XML declaration. Since we explicitly test support for that case,
    # skip initial whitespace.
    baseparser.matchseq(b'')
    stream = baseparser.remainder()
    try:
        if isinstance(stream, io.BytesIO):
            # Empirically, fromstring() seems faster than _parse(). If passed
            # a BytesIO, extract its contents and skip to BytesIO read pos.
            element = fromstring(stream.getvalue()[stream.tell():])
        else:
            # Not a BytesIO, parse the stream
            element = _parse(stream).getroot()
    except ElementTreeError as err:
        raise LLSDParseError(*err.args)

    # We expect that the outer-level XML element is <llsd>...</llsd>.
    if element.tag != 'llsd':
        raise LLSDParseError("Invalid XML Declaration")
    # Extract its contents.
    return LLSDXMLParser().parse_node(element[0])


def format_xml(something):
    """
    Format a python object as application/llsd+xml

    :param something: a python object (typically a dict) to be serialized.
    :returns: Returns an XML formatted string.

    See http://wiki.secondlife.com/wiki/LLSD#XML_Serialization
    """
    return LLSDXMLFormatter().format(something)


def write_xml(stream, something):
    """
    Serialize to passed 'stream' the python object 'something' as
    application/llsd+xml.

    :param stream: a binary stream open for writing.
    :param something: a python object (typically a dict) to be serialized.

    See http://wiki.secondlife.com/wiki/LLSD#XML_Serialization
    """
    return LLSDXMLFormatter().write(stream, something)
