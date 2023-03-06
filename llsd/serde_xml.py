import base64
import re
import types

from llsd.base import (_LLSD, ALL_CHARS, LLSDBaseFormatter, LLSDParseError,
                       LLSDSerializationError, UnicodeType,
                       _format_datestr, _str_to_bytes, _to_python, is_unicode)
from llsd.fastest_elementtree import ElementTreeError, fromstring

INVALID_XML_BYTES = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c'\
                    b'\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18'\
                    b'\x19\x1a\x1b\x1c\x1d\x1e\x1f'
INVALID_XML_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')


def remove_invalid_xml_bytes(b):
    try:
        # Dropping chars that cannot be parsed later on.  The
        # translate() function was benchmarked to be the fastest way
        # to do this.
        return b.translate(ALL_CHARS, INVALID_XML_BYTES)
    except TypeError:
        # we get here if s is a unicode object (should be limited to
        # unit tests)
        return INVALID_XML_RE.sub('', b)


class LLSDXMLFormatter(LLSDBaseFormatter):
    """
    Class which implements LLSD XML serialization.

    http://wiki.secondlife.com/wiki/LLSD#XML_Serialization

    This class serializes a limited subset of python objects as
    application/llsd+xml. You do not generally need to make an instance of
    this class since the module level format_xml() is the most convenient
    interface to this functionality.
    """
    def _elt(self, name, contents=None):
        """
        Serialize a single element.

        If 'contents' is omitted, write <name/>.
        If 'contents' is bytes, write <name>contents</name>.
        If 'contents' is str, write <name>contents.encode('utf8')</name>.
        If 'contents' is callable, write <name>, call contents(), write </name>.
        """
        if not contents:
            self.stream.writelines([b"<", name, b" />"])
        else:
            self.stream.writelines([b"<", name, b">"])
            if callable(contents):
                contents()
            else:
                self.stream.write(_str_to_bytes(contents))
            self.stream.writelines([b"</", name, b">"])

    def xml_esc(self, v):
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

    def LLSD(self, v):
        return self._generate(v.thing)
    def UNDEF(self, _v):
        return self._elt(b'undef')
    def BOOLEAN(self, v):
        if v:
            return self._elt(b'boolean', b'true')
        else:
            return self._elt(b'boolean', b'false')
    def INTEGER(self, v):
        return self._elt(b'integer', str(v))
    def REAL(self, v):
        return self._elt(b'real', repr(v))
    def UUID(self, v):
        if v.int == 0:
            return self._elt(b'uuid')
        else:
            return self._elt(b'uuid', str(v))
    def BINARY(self, v):
        return self._elt(b'binary', base64.b64encode(v).strip())
    def STRING(self, v):
        return self._elt(b'string', self.xml_esc(v))
    def URI(self, v):
        return self._elt(b'uri', self.xml_esc(str(v)))
    def DATE(self, v):
        return self._elt(b'date', _format_datestr(v))
    def ARRAY(self, v):
        return self._elt(
            b'array',
            lambda: [self._generate(item) for item in v])
    def MAP(self, v):
        return self._elt(
            b'map',
            lambda: [(self._elt(b'key', self.xml_esc(UnicodeType(key))),
                      self._generate(value))
                     for key, value in v.items()])

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
        self.stream.write(b'<?xml version="1.0" ?>')
        self._elt(b"llsd", lambda: self._generate(something))


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

    def _indent(self):
        "Write an indentation based on the atom and indentation level."
        self.stream.writelines([self._indent_atom] * self._indent_level)

    def ARRAY(self, v):
        "Recursively format an array with pretty turned on."
        self.stream.write(b'<array>\n')
        self._indent_level += 1
        for item in v:
            self._indent()
            self._generate(item)
            self.stream.write(b'\n')
        self._indent_level -= 1
        self._indent()
        self.stream.write(b'</array>')

    def MAP(self, v):
        "Recursively format a map with pretty turned on."
        self.stream.write(b'<map>\n')
        self._indent_level += 1
        # sorted list of keys
        for key in sorted(v):
            self._indent()
            self._elt(b'key', UnicodeType(key))
            self.stream.write(b'\n')
            self._indent()
            self._generate(v[key])
            self.stream.write(b'\n')
        self._indent_level -= 1
        self._indent()
        self.stream.write(b'</map>')

    def _write(self, something):
        """
        Serialize a python object to self.stream as 'pretty' application/llsd+xml.

        :param something: a python object (typically a dict) to be serialized.
        """
        self.stream.write(b'<?xml version="1.0" ?>\n<llsd>')
        self._generate(something)
        self.stream.write(b'</llsd>\n')


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


declaration_regex = re.compile(br'^\s*(?:<\?[\x09\x0A\x0D\x20-\x7e]+\?>)|(?:<llsd>)')
def validate_xml_declaration(something):
    if not declaration_regex.match(something):
        raise LLSDParseError("Invalid XML Declaration")


def parse_xml(something):
    """
    This is the basic public interface for parsing llsd+xml.

    :param something: The data to parse.
    :returns: Returns a python object.
    """
    try:
        # validate xml declaration manually until http://bugs.python.org/issue7138 is fixed
        validate_xml_declaration(something)
        return _to_python(fromstring(something)[0])
    except ElementTreeError as err:
        raise LLSDParseError(*err.args)


_g_xml_formatter = None
def _get_xml_formatter():
    global _g_xml_formatter
    if _g_xml_formatter is None:
        _g_xml_formatter = LLSDXMLFormatter()
    return _g_xml_formatter


def format_xml(something):
    """
    Format a python object as application/llsd+xml

    :param something: a python object (typically a dict) to be serialized.
    :returns: Returns an XML formatted string.

    See http://wiki.secondlife.com/wiki/LLSD#XML_Serialization
    """
    return _get_xml_formatter().format(something)


def write_xml(stream, something):
    """
    Serialize to passed 'stream' the python object 'something' as
    application/llsd+xml.

    :param stream: a binary stream open for writing.
    :param something: a python object (typically a dict) to be serialized.

    See http://wiki.secondlife.com/wiki/LLSD#XML_Serialization
    """
    return _get_xml_formatter().write(stream, something)
