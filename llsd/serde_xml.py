import base64
import io
import re
import types

from llsd.base import (_LLSD, ALL_CHARS, LLSDBaseParser, LLSDBaseFormatter, XML_HEADER,
                       LLSDParseError, LLSDSerializationError, UnicodeType,
                       _format_datestr, _str_to_bytes, _to_python, is_unicode, PY2)
from llsd.fastest_elementtree import ElementTreeError, fromstring, parse as _parse

INVALID_XML_BYTES = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c'\
                    b'\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18'\
                    b'\x19\x1a\x1b\x1c\x1d\x1e\x1f'

XML_ESC_TRANS = {}
if not PY2:
    XML_ESC_TRANS = str.maketrans({'&': '&amp;',
                                   '<':'&lt;',
                                   '>':'&gt;',
                                   u'\uffff':None,   # cannot be parsed
                                   u'\ufffe':None})  # cannot be parsed

    for x in INVALID_XML_BYTES:
        XML_ESC_TRANS[x] = None

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

def xml_esc(v):
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
        "Construct a pretty serializer."
        # Call the super class constructor so that we have the type map
        super(LLSDXMLFormatter, self).__init__()
        self.py2 = PY2
        
    def _LLSD(self, v):
        raise LLSDSerializationError("We should never end up here")
    def _UNDEF(self, _v):
        return b'<undef/>'
    def _BOOLEAN(self, v):
        if v:
            return b'<boolean>true</boolean>'
        return b'<boolean>false</boolean>'
    def _INTEGER(self, v):
        return b'<integer>' + str(v).encode('utf-8') + b'</integer>'
    def _REAL(self, v):
        return b'<real>' + str(v).encode('utf-8') + b'</real>'
    def _UUID(self, v):
        if v.int == 0:
            return b'<uuid/>'
        else:
            return b'<uuid>' + str(v).encode('utf-8') + b'</uuid>'
    def _BINARY(self, v):
        return b'<binary>' + base64.b64encode(v).strip() + b'</binary>'
    def _STRING(self, v):
        if self.py2:
            return b'<string>' + _str_to_bytes(xml_esc(v)) + b'</string>'
        else:
            return b'<string>' + v.translate(XML_ESC_TRANS).encode('utf-8') + b'</string>'
    def _URI(self, v):
        if self.py2:
            return b'<uri>' + _str_to_bytes(xml_esc(v)) + b'</uri>'
        else:
            return b'<uri>' + UnicodeType(v).translate(XML_ESC_TRANS).encode('utf-8') + b'</uri>'
    def _DATE(self, v):
        return b'<date>' + _format_datestr(v) + b'</date>'
    def _ARRAY(self, v):
        raise LLSDSerializationError("We should never end up here")
    def _MAP(self, v):
        raise LLSDSerializationError("We should never end up here")

    def _write(self, something):
        """
        Serialize a python object to self.stream as application/llsd+xml.

        :param something: A python object (typically a dict) to be serialized.
        """
        self.stream.write(b'<?xml version="1.0" ?>'
                          b'<llsd>')

        iter_stack = [(iter([something]), b"", None)]
        while True:
            cur_iter, iter_type, iterable_obj = iter_stack[-1]
            try:
                item = next(cur_iter)
                if iter_type == b"map":

                    if self.py2:
                        self.stream.write(b'<key>' +
                                          _str_to_bytes(xml_esc(UnicodeType(item))) +
                                          b'</key>')
                    else:
                        # fair performance improvement by explicitly doing the
                        # translate for py3 instead of calling xml_esc
                        self.stream.write(b'<key>' +
                        UnicodeType(item).translate(XML_ESC_TRANS).encode('utf-8') +
                                          b'</key>')
                    item = iterable_obj[item]
                if isinstance(item, _LLSD):
                    item = item.thing
                item_type = type(item)
                if not item_type in self.type_map:
                    raise LLSDSerializationError(
                        "Cannot serialize unknown type: %s (%s)" % (item_type, item))
                tfunction = self.type_map[item_type]

                if tfunction == self._MAP:
                    self.stream.write(b'<map>')
                    iter_stack.append((iter(list(item)), b"map", item))
                elif tfunction == self._ARRAY:
                    self.stream.write(b'<array>')
                    iter_stack.append((iter(item), b"array", None))
                else:
                    self.stream.write(tfunction(item))
            except StopIteration:
                self.stream.write(b'</' + iter_type + b'>')
                iter_stack.pop()
            if len(iter_stack) == 1:
                break
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

    def _indent(self):
        "Write an indentation based on the atom and indentation level."
        self.stream.writelines([self._indent_atom] * self._indent_level)

    def _write(self, something):
        """
        Serialize a python object to self.stream as application/llsd+xml.

        :param something: A python object (typically a dict) to be serialized.

        NOTE: This is nearly identical to the above _write with the exception
        that this one includes newlines and indentation.  Doing something clever
        for the above may decrease performance for the common case, so it's been
        split out.  We can probably revisit this, though.
        """
        self.stream.write(b'<?xml version="1.0" ?>\n'
                          b'<llsd>\n')

        iter_stack = [(iter([something]), b"", None)]
        while True:
            cur_iter, iter_type, iterable_obj = iter_stack[-1]
            try:
                item = next(cur_iter)
                if iter_type == b"map":
                    self._indent()
                    if self.py2:
                        self.stream.write(b'<key>' +
                                          _str_to_bytes(xml_esc(UnicodeType(item))) +
                                          b'</key>')
                    else:
                        # calling translate directly is a bit faster
                        self.stream.write(b'<key>' +
                        UnicodeType(item).translate(XML_ESC_TRANS).encode('utf-8') +
                                          b'</key>\n')
                    item = iterable_obj[item]
                if isinstance(item, _LLSD):
                    item = item.thing
                item_type = type(item)
                if not item_type in self.type_map:
                    raise LLSDSerializationError(
                        "Cannot serialize unknown type: %s (%s)" % (item_type, item))
                tfunction = self.type_map[item_type]

                if tfunction == self._MAP:
                    self._indent()
                    self.stream.write(b'<map>\n')
                    self._indent_level += 1
                    iter_stack.append((iter(list(item)), b"map", item))
                elif tfunction == self._ARRAY:
                    self._indent()
                    self.stream.write(b'<array>\n')
                    self._indent_level += 1
                    iter_stack.append((iter(item), b"array", None))
                else:
                    self._indent()
                    self.stream.write(tfunction(item))
                    self.stream.write(b'\n')
            except StopIteration:
                self._indent_level -= 1
                self._indent()
                self.stream.write(b'</' + iter_type + b'>\n')
                iter_stack.pop()
            if len(iter_stack) == 1:
                break
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
    return _to_python(element[0])


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
