"""
Types as well as parsing and formatting functions for handling LLSD.

This is the llsd module -- parsers and formatters between the
supported subset of mime types and python objects. Documentation
available on the Second Life wiki:

http://wiki.secondlife.com/wiki/LLSD
"""
from llsd.base import (_LLSD, BINARY_MIME_TYPE, NOTATION_MIME_TYPE, XML_MIME_TYPE, LLSDParseError,
                       LLSDSerializationError, LongType, UnicodeType, binary, starts_with, undef, uri)
from llsd.serde_binary import LLSDBinaryParser, format_binary, parse_binary, match_binary_hdr, parse_binary_noh
from llsd.serde_notation import LLSDNotationFormatter, LLSDNotationParser, format_notation, parse_notation, match_notation_hdr, parse_notation_noh
from llsd.serde_xml import LLSDXMLFormatter, LLSDXMLPrettyFormatter, format_pretty_xml, format_xml, parse_xml, match_xml_hdr, parse_xml_noh


def parse(something, mime_type = None):
    """
    This is the basic public interface for parsing llsd.

    :param something: The data to parse. This is expected to be bytes, not
           strings, or a byte stream.
    :param mime_type: The mime_type of the data if it is known.
    :returns: Returns a python object.

    Python 3 Note: when reading LLSD from a file, use open()'s 'rb' mode explicitly
    """
    try:
        if mime_type:
            # explicit mime_type -- 'something' may or may not also have a header
            for mime_types, parser in (
                    ({XML_MIME_TYPE, 'application/llsd'}, parse_xml),
                    ({BINARY_MIME_TYPE},                  parse_binary),
                    ({NOTATION_MIME_TYPE},                parse_notation),
##                  ({'application/json'},                parse_notation),
                    ):
                if mime_type.lower() in mime_types:
                    return parser(something)

        # no recognized mime type, look for header
        for matcher, parser in (
                (match_binary_hdr,   parse_binary_noh),
                (match_notation_hdr, parse_notation_noh),
                (match_xml_hdr,      parse_xml_noh),
                ):
            remainder = matcher(something)
            if remainder is not None:
                # we already saw the header, don't check again
                return parser(remainder)

        # no recognized header -- does content resemble XML?
        if starts_with(b'<', something):
            return parse_xml_noh(something)
        else:
            return parse_notation_noh(something)

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
