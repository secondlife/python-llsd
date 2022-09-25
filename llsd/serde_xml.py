import base64
import re
import types

from llsd.base import (_LLSD, ALL_CHARS, B, LLSDBaseFormatter, LLSDParseError, LLSDSerializationError, UnicodeType,
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
    Class which implements LLSD XML serialization..

    http://wiki.secondlife.com/wiki/LLSD#XML_Serialization

    This class wraps both a pure python and c-extension for formatting
    a limited subset of python objects as application/llsd+xml. You do
    not generally need to make an instance of this object since the
    module level format_xml is the most convenient interface to this
    functionality.
    """

    def _elt(self, name, contents=None):
        "Serialize a single element."
        if not contents:
            return B("<%s />") % (name,)
        else:
            return B("<%s>%s</%s>") % (name, _str_to_bytes(contents), name)

    def xml_esc(self, v):
        "Escape string or unicode object v for xml output"

        # Use is_unicode() instead of is_string() because in python 2, str is
        # bytes, not unicode, and should not be "encode()"'d. attempts to
        # encode("utf-8") a bytes type will result in an implicit
        # decode("ascii") that will throw a UnicodeDecodeError if the string
        # contains non-ascii characters
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
            b''.join([self._generate(item) for item in v]))
    def MAP(self, v):
        return self._elt(
            b'map',
            b''.join([B("%s%s") % (self._elt(b'key', self.xml_esc(UnicodeType(key))),
                               self._generate(value))
             for key, value in v.items()]))

    typeof = type
    def _generate(self, something):
        "Generate xml from a single python object."
        t = self.typeof(something)
        if t in self.type_map:
            return self.type_map[t](something)
        elif isinstance(something, _LLSD):
            return self.type_map[_LLSD](something)
        else:
            raise LLSDSerializationError(
                "Cannot serialize unknown type: %s (%s)" % (t, something))

    def _format(self, something):
        "Pure Python implementation of the formatter."
        return b'<?xml version="1.0" ?>' + self._elt(b"llsd", self._generate(something))

    def format(self, something):
        """
        Format a python object as application/llsd+xml

        :param something: A python object (typically a dict) to be serialized.
        :returns: Returns an XML formatted string.
        """
        return self._format(something)

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

        # Override the type map to use our specialized formatters to
        # emit the pretty output.
        self.type_map[list] = self.PRETTY_ARRAY
        self.type_map[tuple] = self.PRETTY_ARRAY
        self.type_map[types.GeneratorType] = self.PRETTY_ARRAY,
        self.type_map[dict] = self.PRETTY_MAP

        # Private data used for indentation.
        self._indent_level = 1
        if indent_atom is None:
            self._indent_atom = b'  '
        else:
            self._indent_atom = indent_atom

    def _indent(self):
        "Return an indentation based on the atom and indentation level."
        return self._indent_atom * self._indent_level

    def PRETTY_ARRAY(self, v):
        "Recursively format an array with pretty turned on."
        rv = []
        rv.append(b'<array>\n')
        self._indent_level = self._indent_level + 1
        rv.extend([B("%s%s\n") %
                   (self._indent(),
                    self._generate(item))
                   for item in v])
        self._indent_level = self._indent_level - 1
        rv.append(self._indent())
        rv.append(b'</array>')
        return b''.join(rv)

    def PRETTY_MAP(self, v):
        "Recursively format a map with pretty turned on."
        rv = []
        rv.append(b'<map>\n')
        self._indent_level = self._indent_level + 1
        # list of keys
        keys = list(v)
        keys.sort()
        rv.extend([B("%s%s\n%s%s\n") %
                   (self._indent(),
                    self._elt(b'key', UnicodeType(key)),
                    self._indent(),
                    self._generate(v[key]))
                   for key in keys])
        self._indent_level = self._indent_level - 1
        rv.append(self._indent())
        rv.append(b'</map>')
        return b''.join(rv)

    def format(self, something):
        """
        Format a python object as application/llsd+xml

        :param something: a python object (typically a dict) to be serialized.
        :returns: Returns an XML formatted string.
        """
        data = []
        data.append(b'<?xml version="1.0" ?>\n<llsd>')
        data.append(self._generate(something))
        data.append(b'</llsd>\n')
        return b'\n'.join(data)


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
def format_xml(something):
    """
    Format a python object as application/llsd+xml

    :param something: a python object (typically a dict) to be serialized.
    :returns: Returns an XML formatted string.

    Ssee http://wiki.secondlife.com/wiki/LLSD#XML_Serialization

    This function wraps both a pure python and c-extension for formatting
    a limited subset of python objects as application/llsd+xml.
    """
    global _g_xml_formatter
    if _g_xml_formatter is None:
        _g_xml_formatter = LLSDXMLFormatter()
    return _g_xml_formatter.format(something)