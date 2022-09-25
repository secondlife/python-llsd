"""
Types as well as parsing and formatting functions for handling LLSD.

This is the llsd module -- parsers and formatters between the
supported subset of mime types and python objects. Documentation
available on the Second Life wiki:

http://wiki.secondlife.com/wiki/LLSD
"""
from llsd.base import (_LLSD, BINARY_MIME_TYPE, NOTATION_MIME_TYPE, XML_MIME_TYPE, LLSDParseError,
                       LLSDSerializationError, LongType, UnicodeType, binary, starts_with, undef, uri)
from llsd.serde_binary import format_binary, parse_binary
from llsd.serde_notation import format_notation, parse_notation
from llsd.serde_xml import format_pretty_xml, format_xml, parse_xml

__all__ = [
    "BINARY_MIME_TYPE",
    "LLSD",
    "LLSDParseError",
    "LLSDSerializationError",
    "LongType",
    "NOTATION_MIME_TYPE",
    "UnicodeType",
    "XML_MIME_TYPE",
    "binary",
    "format_binary",
    "format_notation",
    "format_pretty_xml",
    "format_xml",
    "parse",
    "parse_binary",
    "parse_notation",
    "parse_xml",
    "undef",
    "uri",
]


def parse(something, mime_type = None):
    """
    This is the basic public interface for parsing llsd.

    :param something: The data to parse. This is expected to be bytes, not strings
    :param mime_type: The mime_type of the data if it is known.
    :returns: Returns a python object.

    Python 3 Note: when reading LLSD from a file, use open()'s 'rb' mode explicitly
    """
    if mime_type in (XML_MIME_TYPE, 'application/llsd'):
        return parse_xml(something)
    elif mime_type == BINARY_MIME_TYPE:
        return parse_binary(something)
    elif mime_type == NOTATION_MIME_TYPE:
        return parse_notation(something)
    #elif content_type == 'application/json':
    #    return parse_notation(something)
    try:
        something = something.lstrip()   #remove any pre-trailing whitespace
        if starts_with(b'<?llsd/binary?>', something):
            return parse_binary(something)
        # This should be better.
        elif starts_with(b'<', something):
            return parse_xml(something)
        else:
            return parse_notation(something)
    except KeyError as e:
        raise LLSDParseError('LLSD could not be parsed: %s' % (e,))
    except TypeError as e:
        raise LLSDParseError('Input stream not of type bytes. %s' % (e,))


class LLSD(_LLSD):
    def __bytes__(self):
        return self.as_xml(self.thing)


    def __str__(self):
        return self.__bytes__().decode()

    parse = staticmethod(parse)
    as_xml = staticmethod(format_xml)
    as_pretty_xml = staticmethod(format_pretty_xml)
    as_binary = staticmethod(format_binary)
    as_notation = staticmethod(format_notation)