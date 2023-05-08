
# -*- coding: utf-8 -*-
from __future__ import print_function

import base64
from datetime import date, datetime
import io
from itertools import islice
import pprint
import re
import struct
import time
import unittest
import uuid

import pytest

import llsd
from llsd.base import PY2, is_integer, is_string, is_unicode
from llsd.serde_xml import remove_invalid_xml_bytes
from tests.fuzz import LLSDFuzzer


class Foo(object):
    """
    Simple Mock Class used for testing.
    """
    pass

try:
    from math import isnan as _isnan
    def isnan(x):
        if isinstance(x, float):
            return _isnan(x)
        else:
            return False
except ImportError:
    def isnan(x):
        return x != x


class LLSDNotationUnitTest(unittest.TestCase):
    """
    This class aggregates all the tests for parse_notation(something),
    LLSD.as_notation(something) and format_notation (i.e. same as
    LLSD.as_notation(something).  Note that test scenarios for the
    same input type are all put into single test method. And utility
    method assert_notation_roundtrip is used to test parse_notation
    and as_notation at the same time.
    """
    def setUp(self):
        """
        Set up the test class
        """
        self.llsd = llsd.LLSD()

    def strip(self, the_string):
        """
        Remove any whitespace characters from the input string.

        :Parameters:
        - 'the_string': string to remove the whitespaces.
        """
        return re.sub(br'\s', b'', the_string)

    def assertNotationRoundtrip(self, py_in, str_in, is_alternate_notation=False):
        """
        Utility method to check the result of parse_notation and
        LLSD.as_notation.
        """
        # use parse to check here
        py_out = self.llsd.parse(str_in)
        py_out2 = self.llsd.parse(io.BytesIO(str_in))
        self.assertEqual(py_out2, py_out)
        str_out = self.llsd.as_notation(py_in)
        py_roundtrip = self.llsd.parse(str_out)
        py_roundtrip2 = self.llsd.parse(io.BytesIO(str_out))
        self.assertEqual(py_roundtrip2, py_roundtrip)
        str_roundtrip = self.llsd.as_notation(py_out)
        # compare user-passed Python data with parsed user-passed string
        self.assertEqual(py_in, py_out)
        # compare user-passed Python data with parsed (serialized data)
        self.assertEqual(py_in, py_roundtrip)

##      # Comparing serialized data invites exasperating spurious test
##      # failures. Most interesting LLSD data is contained in dicts, and
##      # Python has never guaranteed the serialization order of dict keys.
##      # If str_in is an alternate notation, we can't compare it directly.
##      if not is_alternate_notation:
##          self.assertEqual(self.strip(str_out), self.strip(str_in))
##      self.assertEqual(self.strip(str_out), self.strip(str_roundtrip))

        # use parse_notation to check again
        py_out = llsd.parse_notation(str_in)
        str_out = self.llsd.as_notation(py_in)
        py_roundtrip = llsd.parse_notation(str_out)
        str_roundtrip = self.llsd.as_notation(py_out)
        self.assertEqual(py_in, py_out)
        self.assertEqual(py_in, py_roundtrip)

##      # Disabled for the same reason as above.
##      # If str_in is an alternate notation, we can't compare it directly.
##      if not is_alternate_notation:
##          self.assertEqual(self.strip(str_out), self.strip(str_in))
##      self.assertEqual(self.strip(str_out), self.strip(str_roundtrip))

    def testInteger(self):
        """
        Test the input type integer.
        Maps to test scenarios module:llsd:test#4-6
        """
        pos_int_notation = b"i123456"
        neg_int_notation = b"i-123457890"
        blank_int_notation = b"i0"

        python_pos_int = 123456
        python_neg_int = -123457890

        self.assertNotationRoundtrip(python_pos_int,
                                       pos_int_notation)
        self.assertNotationRoundtrip(python_neg_int,
                                       neg_int_notation)
        self.assertEqual(0, self.llsd.parse(blank_int_notation))

    def testUndefined(self):
        """
        Test the input type : undef
        Maps to test scenarios module:llsd:test#7
        """
        undef_notation = b"!"
        self.assertNotationRoundtrip(None, undef_notation)

    def testBoolean(self):
        """
        Test the input type : Boolean
        Maps to test scenarios module:llsd:test#8-17
        """
        sample_data = [(True, b"TRUE"),
            (True, b"true"),
            (True, b"T"),
            (True, b"t"),
            (True, b"1"),
            (False, b"FALSE"),
            (False, b"false"),
            (False, b"F"),
            (False, b"f"),
            (False, b"0")
        ]
        for py, notation in sample_data:
            is_alternate_notation = False
            if notation not in (b"true", b"false"):
                is_alternate_notation = True
            self.assertNotationRoundtrip(py, notation, is_alternate_notation)

        blank_notation = b""
        self.assertEqual(False, self.llsd.parse(blank_notation))

    def testReal(self):
        """
        Test the input type: real.
        Maps to test scenarios module:llsd:test#18-20
        """
        pos_real_notation = b"r2983287453.3000002"
        neg_real_notation = b"r-2983287453.3000002"
        blank_real_notation = b"r0"

        python_pos_real = 2983287453.3
        python_neg_real = -2983287453.3

        self.assertNotationRoundtrip(python_pos_real,
                                       pos_real_notation, True)
        self.assertNotationRoundtrip(python_neg_real,
                                       neg_real_notation, True)
        self.assertEqual(0, self.llsd.parse(blank_real_notation))


    def testUUID(self):
        """
        Test the input type : UUID.
        Maps to test scenarios module:llsd:test#21
        """
        uuid_tests = {
            uuid.UUID(hex='d7f4aeca-88f1-42a1-b385-b9db18abb255'):b"ud7f4aeca-88f1-42a1-b385-b9db18abb255",
            uuid.UUID(hex='00000000-0000-0000-0000-000000000000'):b"u00000000-0000-0000-0000-000000000000"}

        for py, notation in uuid_tests.items():
            self.assertNotationRoundtrip(py, notation)

    def testString(self):
        """
        Test the input type: String.
        Maps to test scenarios module:llsd:test#22-24
        """
        sample_data = [('foo bar magic" go!', b"'foo bar magic\" go!'"),
            ("foo bar magic's go!", b'"foo bar magic\'s go!"'),
            ('have a nice day', b"'have a nice day'"),
            ('have a nice day', b'"have a nice day"'),
            ('have a nice day', b's(15)"have a nice day"'),
            ('have a "nice" day', b'\'have a "nice" day\''),
            ('have a "nice" day', b'"have a \\"nice\\" day"'),
            ('have a "nice" day', b's(17)"have a "nice" day"'),
            ("have a 'nice' day", b"'have a \\'nice\\' day'"),
            ("have a 'nice' day", b'"have a \'nice\' day"'),
            ("have a 'nice' day", b's(17)"have a \'nice\' day"'),
            (u"Kanji: '\u5c0f\u5fc3\u8005'",
             b"'Kanji: \\'\xe5\xb0\x8f\xe5\xbf\x83\xe8\x80\x85\\''"),
            (u"Kanji: '\u5c0f\u5fc3\u8005'",
             b"\"Kanji: '\\xe5\\xb0\\x8f\\xE5\\xbf\\x83\\xe8\\x80\\x85'\""),
             ('\a\b\f\n\r\t\v', b'"\\a\\b\\f\\n\\r\\t\\v"')
        ]
        for py, notation in sample_data:
            is_alternate_notation = False
            if notation[0:1] != "'":
                is_alternate_notation = True
            self.assertNotationRoundtrip(py, notation, is_alternate_notation)

    def testURI(self):
        """
        Test the input type: URI.
        Maps to test scenarios module:llsd:test#25 - 26
        """
        uri_tests = {
            llsd.uri('http://www.topcoder.com/tc/projects?id=1230'):b'l"http://www.topcoder.com/tc/projects?id=1230"',
            llsd.uri('http://www.topcoder.com/tc/projects?id=1231'):b"l'http://www.topcoder.com/tc/projects?id=1231'"}

        blank_uri_notation = b'l""'

        for py, notation in uri_tests.items():
            is_alternate_notation = False
            if notation[1:2] != b'"':
                is_alternate_notation = True
            self.assertNotationRoundtrip(py, notation, is_alternate_notation)
        self.assertEqual('', self.llsd.parse(blank_uri_notation))

    def testDate(self):
        """
        Test the input type : Date.
        Maps to test scenarios module:llsd:test#27 - 30
        """
        valid_date_notation = b'd"2006-02-01T14:29:53.460000Z"'
        valid_date_notation_no_float = b'd"2006-02-01T14:29:53Z"'
        valid_date_notation_zero_seconds = b'd"2006-02-01T14:29:00Z"'
        valid_date_notation_filled = b'd"2006-02-01T14:29:05Z"'
        valid_date_19th_century = b'd"1833-02-01T00:00:00Z"'

        blank_date_notation = b'd""'

        python_valid_date = datetime(2006, 2, 1, 14, 29, 53, 460000)
        python_valid_date_no_float = datetime(2006, 2, 1, 14, 29, 53)
        python_valid_date_zero_seconds = datetime(2006, 2, 1, 14, 29, 0)
        python_valid_date_filled = datetime(2006, 2, 1, 14, 29, 5)
        python_valid_date_19th_century = datetime(1833,2,1)

        python_blank_date = datetime(1970, 1, 1)

        self.assertNotationRoundtrip(python_valid_date,
                                       valid_date_notation)
        self.assertNotationRoundtrip(python_valid_date_no_float,
                                       valid_date_notation_no_float)
        self.assertNotationRoundtrip(python_valid_date_zero_seconds,
                                       valid_date_notation_zero_seconds)
        self.assertNotationRoundtrip(python_valid_date_filled,
                                       valid_date_notation_filled)

        self.assertNotationRoundtrip(python_valid_date_filled,
                                       valid_date_notation_filled)
        self.assertNotationRoundtrip(python_valid_date_19th_century,
                                        valid_date_19th_century)

        self.assertEqual(python_blank_date, self.llsd.parse(blank_date_notation))

    def testArray(self):
        """
        Test the input type : Array.
        Maps to test scenarios module:llsd:test#31-33
        """
        # simple array
        array_notation = b"['foo', 'bar']"
        # composite array
        array_within_array_notation = b"['foo', 'bar',['foo', 'bar']]"
        # blank array
        blank_array_notation = b"[]"

        python_array = [str("foo"), "bar"]
        python_array_within_array = ["foo", "bar", ["foo", "bar"]]
        python_blank_array = []

        self.assertNotationRoundtrip(python_array, array_notation)
        self.assertNotationRoundtrip(python_array_within_array,
                                       array_within_array_notation)
        self.assertNotationRoundtrip(python_blank_array, blank_array_notation)

    def testMap(self):
        """
        Test the input type : Map.
        Maps to test scenarios module:llsd:test#34-36
        """
        # simple map
        map_notation = b"{'foo':'bar'}"

        # composite map
        map_within_map_notation = b"{'foo':'bar','doo':{'goo':'poo'}}"

        # blank map
        blank_map_notation = b"{}"

        python_map = {"foo":"bar"}
        python_map_within_map = {"foo":"bar", "doo":{"goo":"poo"}}
        python_blank_map = {}

        self.assertNotationRoundtrip(python_map, map_notation)
        self.assertNotationRoundtrip(python_map_within_map,
                                       map_within_map_notation)
        self.assertNotationRoundtrip(python_blank_map, blank_map_notation)

    def testBinary(self):
        """
        Test the input type: binary.
        Maps to test scenarios module:llsd:test#37
        """
        string_data1 = b"quick brown fox!!"
        string_data2 = b"""
                <p>"Take some more <a href="/wiki/Tea" title="Tea">tea</a> ," the March Hare said to Alice, very earnestly.</p>
                """
        python_binary1 = llsd.binary(string_data1)
        python_binary2 = llsd.binary(string_data2)

        notation1 = b'b64' + b'"' + base64.b64encode(string_data1).strip() + b'"'
        notation2 = b'b64' + b'"' + base64.b64encode(string_data2).strip() + b'"'
        notation3 = b'b16' + b'"' + base64.b16encode(string_data1).strip() + b'"'
        notation4 = b'b16' + b'"' + base64.b16encode(string_data2).strip() + b'"'
        notation5 = b'b85' + b'"<~EHPu*CER),Dg-(AAoDo;+T~>"'
        notation6 = b'b85' +br'"<~4E*J.<+0QR+EMI<AKYi.Eb-@U@3B6(AS+(L06_,GBeNFs@3Qh9Bln0&4X*j:@3RmWARR\S@6Peb+s:u@AKX]UEarc*87?OM+ELt*A0>u4+@0gX@q@26G%G]>+D"u%DImm2Cj@Wq05s)~>"'

        self.assertNotationRoundtrip(python_binary1, notation1, True)
        self.assertNotationRoundtrip(python_binary2, notation2, True)
        self.assertNotationRoundtrip(python_binary1, notation3, True)
        self.assertNotationRoundtrip(python_binary2, notation4, True)
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, notation5)
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, notation6)

    '''
    def testProblemMap(self):
        """
        This is some data that the fuzzer generated that caused a parse error
        """
        string_data = b"{'$g7N':!,'3r=h':true,'\xe8\x88\xbc\xe9\xa7\xb9\xe1\xb9\xa6\xea\xb3\x95\xe0\xa8\xb3\xe1\x9b\x84\xef\xb2\xa7\xe8\x8f\x99\xe8\x94\xa0\xe9\x90\xb9\xe6\x88\x9b\xe0\xaf\x84\xe8\xb8\xa2\xe4\x94\x83\xea\xb5\x8b\xed\x8c\x8a\xe5\xb5\x97':'\xe6\xbb\xa6\xe3\xbf\x88\xea\x9b\x82\xea\x9f\x8d\xee\xbb\xba\xe4\xbf\x87\xe3\x8c\xb5\xe3\xb2\xb0\xe7\x90\x91\xee\x8f\xab\xee\x81\xa5\xea\x94\x98'}"
        python_obj = {}

        import pdb; pdb.set_trace()
        self.assertNotationRoundtrip(python_obj, string_data, True)
    '''

    def testNotationOfAllTypes(self):
        """
        Test notation with mixed with all kinds of simple types.
        Maps to test scenarios module:llsd:test#38
        """
        python_object = [{'destination': 'http://secondlife.com'}, {'version':
            1}, {'modification_date': datetime(2006, 2, 1, 14, 29, 53,
                                               460000)}, {'first_name': 'Phoenix', 'last_name': 'Linden', 'granters':
            [uuid.UUID('a2e76fcd-9360-4f6d-a924-000000000003')], 'look_at': [-0.043753,
            -0.999042, 0.0], 'attachment_data': [{'attachment_point':
            2, 'item_id': uuid.UUID('d6852c11-a74e-309a-0462-50533f1ef9b3'),
            'asset_id': uuid.UUID('c69b29b1-8944-58ae-a7c5-2ca7b23e22fb')},
            {'attachment_point': 10, 'item_id':
            uuid.UUID('ff852c22-a74e-309a-0462-50533f1ef900'), 'asset_id':
            uuid.UUID('5868dd20-c25a-47bd-8b4c-dedc99ef9479')}], 'session_id':
            uuid.UUID('2c585cec-038c-40b0-b42e-a25ebab4d132'), 'agent_id':
            uuid.UUID('3c115e51-04f4-523c-9fa6-98aff1034730'), 'circuit_code': 1075,
            'position': [70.9247, 254.378,
            38.7304]}]

        notation = b"""[
          {'destination':'http://secondlife.com'},
          {'version':i1},
          {'modification_date':d"2006-02-01T14:29:53.460000Z"}
          {
            'agent_id':u3c115e51-04f4-523c-9fa6-98aff1034730,
            'session_id':u2c585cec-038c-40b0-b42e-a25ebab4d132,
            'circuit_code':i1075,
            'first_name':'Phoenix',
            'last_name':'Linden',
            'position':[r70.9247,r254.378,r38.7304],
            'look_at':[r-0.043753,r-0.999042,r0.0],
            'granters':[ua2e76fcd-9360-4f6d-a924-000000000003],
            'attachment_data':[
              {
                'attachment_point':i2,
                'item_id':ud6852c11-a74e-309a-0462-50533f1ef9b3,
                'asset_id':uc69b29b1-8944-58ae-a7c5-2ca7b23e22fb
              },
              {
                'attachment_point':i10,
                'item_id':uff852c22-a74e-309a-0462-50533f1ef900,
                'asset_id':u5868dd20-c25a-47bd-8b4c-dedc99ef9479
              }
            ]
          }]"""

        result = self.llsd.parse(notation)
        self.assertEqual(python_object, result)

        # roundtrip test
        notation_result = self.llsd.as_notation(python_object)
        python_object_roundtrip = self.llsd.parse(notation_result)
        self.assertEqual(python_object_roundtrip, python_object)

    def testLLSDSerializationFailure(self):
        """
        Test llsd searialization with non supportd object type.
        TypeError should be raised.

        Maps test scenarios : module:llsd:test#91
        """
        # make an object not supported by llsd
        python_native_obj = Foo()

        # assert than an exception is raised
        self.assertRaises(TypeError, self.llsd.as_notation, python_native_obj)
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b'2')

    def testParseNotationInvalidNotation1(self):
        """
        Test with an invalid array notation.
        Maps to module:llsd:test#76, 86
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"[ 'foo' : 'bar')")

    def testParseNotationInvalidNotation2(self):
        """
        Test with an invalid map notation.
        Maps to module:llsd:test#87
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"{'foo':'bar','doo':{'goo' 'poo'}") # missing separator
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"{'foo':'bar','doo':{'goo' : 'poo'}") # missing closing '}'

    def testParseNotationInvalidNotation3(self):
        """
        Test with an invalid map notation.
        Maps to module:llsd:test#88
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"day day up, day day up")

    def testParseNotationInvalidNotation4(self):
        """
        Test with an invalid date notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b'd"2006#02-01T1429:53.460000Z"')

    def testParseNotationInvalidNotation5(self):
        """
        Test with an invalid int notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b'i*123xx')

    def testParseNotationInvalidNotation6(self):
        """
        Test with an invalid real notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b'r**1.23.3434')

    def testParseNotationInvalidNotation7(self):
        """
        Test with an invalid binary notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"b634'bGFsYQ='")

    def testParseNotationInvalidNotation8(self):
        """
        Test with an invalid map notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"{'foo':'bar',doo':{'goo' 'poo'}}")

    def testParseNotationInvalidNotation9(self):
        """
        Test with an invalid map notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"[i123,i123)")

    def testParseNotationInvalidNotation10(self):
        """
        Test with an invalid raw string notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"s[2]'xx'")

    def testParseNotationInvalidNotation11(self):
        """
        Test with an invalid raw string notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"s(2]'xx'")

    def testParseNotationInvalidNotation12(self):
        """
        Test with an invalid raw string notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"s(2)'xxxxx'")

    def testParseNotationInvalidNotation13(self):
        """
        Test with an invalid raw string notation.
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"s(2)*xx'")

    def testParseNotationIncorrectMIME(self):
        """
        Test with correct notation format but incorrect MIME type. -> llsd:test79
        """
        try:
            self.llsd.parse(b"[ {'foo':'bar'}, {'foo':'bar'} ]", llsd.XML_MIME_TYPE)
            self.fail("LLSDParseError should be raised.")
        except llsd.LLSDParseError:
            pass

    def testParseNotationUnterminatedString(self):
        """
        Test with an unterminated delimited string
        """
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"'foo")

    def testParseNotationHexEscapeNoChars(self):
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"'\\x")

    def testParseNotationHalfTruncatedHex(self):
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"'\\xf")

    def testParseNotationInvalidHex(self):
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b"'\\xzz'")


class LLSDBinaryUnitTest(unittest.TestCase):
    """
    This class aggregates all the tests for parse_binary and LLSD.as_binary
    which is the same as module function format_binary. The tests use roundtrip
    test to check the serialization of llsd object and the parsing of binary
    representation of llsd object.

    Note that llsd binary test scenarios maps to module:llsd:test#66 which reuses
    all the test scenarios of llsd xml.
    """
    def setUp(self):
        """
        Set up the test class, create a LLSD object and assign to self.llsd.
        """
        self.llsd = llsd.LLSD()

    def roundTrip(self, something):
        """
        Utility method which serialize the passed in object using
        binary format, parse the serialized binary format into object, and
        return the object.
        """
        binary = self.llsd.as_binary(something)
        frombytes = self.llsd.parse(binary)
        fromstream = self.llsd.parse(io.BytesIO(binary))
        self.assertEqual(fromstream, frombytes)
        return frombytes

    def testMap(self):
        """
        Test the binary serialization and parse of llsd type : Map.
        """
        map_xml = b"""\
<?xml version="1.0" ?>
<llsd>
<map>
<key>foo</key>
<string>bar</string>
</map>
</llsd>"""

        map_within_map_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<map>\
<key>foo</key>\
<string>bar</string>\
<key>doo</key>\
<map>\
<key>goo</key>\
<string>poo</string>\
</map>\
</map>\
</llsd>"

        blank_map_xml = b"\
<llsd>\
<map />\
</llsd>"

        python_map = {"foo" : "bar"}
        python_map_within_map = {"foo":"bar", "doo":{"goo":"poo"}}

        self.assertEqual(python_map, self.roundTrip(self.llsd.parse(map_xml)))
        self.assertEqual(
            python_map_within_map,
            self.roundTrip(self.llsd.parse(map_within_map_xml)))
        self.assertEqual({}, self.roundTrip(self.llsd.parse(blank_map_xml)))

    def testArray(self):
        """
        Test the binary serialization and parse of llsd type : Array.
        """
        array_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<array>\
<string>foo</string>\
<string>bar</string>\
</array>\
</llsd>"
        array_within_array_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<array>\
<string>foo</string>\
<string>bar</string>\
<array>\
<string>foo</string>\
<string>bar</string>\
</array>\
</array>\
</llsd>"
        blank_array_xml = b"\
<llsd>\
<array />\
</llsd>"

        python_array = ["foo", "bar"]
        python_array_within_array = ["foo", "bar", ["foo", "bar"]]

        self.assertEqual(
            python_array,
            self.roundTrip(self.llsd.parse(array_xml)))
        self.assertEqual(
            python_array_within_array,
            self.roundTrip(self.llsd.parse(array_within_array_xml)))
        self.assertEqual(
            [],
            self.roundTrip(self.llsd.parse(blank_array_xml)))

    def testString(self):
        """
        Test the binary serialization and parse of llsd type : string.
        """
        normal_xml = b"""
<?xml version="1.0" ?>
<llsd>
<string>foo</string>
</llsd>"""

        blank_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<string />\
</llsd>"

        self.assertEqual('foo', self.roundTrip(self.llsd.parse(normal_xml)))
        self.assertEqual("", self.roundTrip(self.llsd.parse(blank_xml)))

    def testInteger(self):
        """
        Test the binary serialization and parse of llsd type : integer
        """
        pos_int_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<integer>289343</integer>\
</llsd>"

        neg_int_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<integer>-289343</integer>\
</llsd>"

        blank_int_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<integer />\
</llsd>"

        python_pos_int = 289343
        python_neg_int = -289343

        self.assertEqual(
            python_pos_int,
            self.roundTrip(self.llsd.parse(pos_int_xml)))
        self.assertEqual(
            python_neg_int,
            self.roundTrip(self.llsd.parse(neg_int_xml)))
        self.assertEqual(
            0,
            self.roundTrip(self.llsd.parse(blank_int_xml)))

    def testReal(self):
        """
        Test the binary serialization and parse of llsd type : real.
        """
        pos_real_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<real>2983287453.3</real>\
</llsd>"

        neg_real_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<real>-2983287453.3</real>\
</llsd>"

        blank_real_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<real />\
</llsd>"

        python_pos_real = 2983287453.3
        python_neg_real = -2983287453.3

        self.assertEqual(
            python_pos_real,
            self.roundTrip(self.llsd.parse(pos_real_xml)))
        self.assertEqual(
            python_neg_real,
            self.roundTrip(self.llsd.parse(neg_real_xml)))
        self.assertEqual(
            0,
            self.roundTrip(self.llsd.parse(blank_real_xml)))

    def testBoolean(self):
        """
        Test the binary serialization and parse of llsd type : boolean.
        """
        true_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<boolean>true</boolean>\
</llsd>"

        false_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<boolean>false</boolean>\
</llsd>"

        blank_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<boolean />\
</llsd>"

        self.assertEqual(True, self.roundTrip(self.llsd.parse(true_xml)))
        self.assertEqual(False, self.roundTrip(self.llsd.parse(false_xml)))
        self.assertEqual(False, self.roundTrip(self.llsd.parse(blank_xml)))

    def testDate(self):
        """
        Test the binary serialization and parse of llsd type : date.
        """
        valid_date_binary = b"d\x00\x00\x40\x78\x31\xf8\xd0\x41"
        valid_date_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<date>2006-02-01T14:29:53Z</date>\
</llsd>"

        blank_date_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<date />\
</llsd>"
        python_valid_date = datetime(2006, 2, 1, 14, 29, 53)
        python_blank_date = datetime(1970, 1, 1)

        self.assertEqual(
            python_valid_date,
            self.roundTrip(self.llsd.parse(valid_date_xml)))
        self.assertEqual(
            python_valid_date,
            self.roundTrip(llsd.parse_binary(valid_date_binary)))
        self.assertEqual(
            python_blank_date,
            self.roundTrip(self.llsd.parse(blank_date_xml)))

    def testBinary(self):
        """
        Test the binary serialization and parse of llsd type : binary.
        """
        base64_binary_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<binary>dGhlIHF1aWNrIGJyb3duIGZveA==</binary>\
</llsd>"

        foo = self.llsd.parse(base64_binary_xml)
        self.assertEqual(
            llsd.binary(b"the quick brown fox"),
            self.roundTrip(foo))

    def testUUID(self):
        """
        Test the binary serialization and parse of llsd type : UUID.
        """
        valid_uuid_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<uuid>d7f4aeca-88f1-42a1-b385-b9db18abb255</uuid>\
</llsd>"
        blank_uuid_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<uuid />\
</llsd>"
        self.assertEqual(
            'd7f4aeca-88f1-42a1-b385-b9db18abb255',
            self.roundTrip(str(self.llsd.parse(valid_uuid_xml))))
        self.assertEqual(
            '00000000-0000-0000-0000-000000000000',
            self.roundTrip(str(self.llsd.parse(blank_uuid_xml))))

        binary_uuid = b"""<?llsd/binary?>\nu\xe1g\xa9D\xd9\x06\x89\x04-\x04\x92\xab\x8e\xaf5\xbf"""

        self.assertEqual(uuid.UUID('e167a944-d906-8904-2d04-92ab8eaf35bf'),
                          llsd.parse(binary_uuid))

    def testURI(self):
        """
        Test the binary serialization and parse of llsd type : URI.
        """
        valid_uri_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<uri>http://sim956.agni.lindenlab.com:12035/runtime/agents</uri>\
</llsd>"

        blank_uri_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<uri />\
</llsd>"

        self.assertEqual(
            'http://sim956.agni.lindenlab.com:12035/runtime/agents',
            self.roundTrip(self.llsd.parse(valid_uri_xml)))
        self.assertEqual(
            '',
            self.roundTrip(self.llsd.parse(blank_uri_xml)))

    def testUndefined(self):
        """
        Test the binary serialization and parse of llsd type : undef.
        """
        undef_xml = b"<?xml version=\"1.0\" ?><llsd><undef /></llsd>"
        self.assertEqual(
            None,
            self.roundTrip(self.llsd.parse(undef_xml)))


    def testBinaryOfAllTypes(self):
        """
        Test the binary serialization and parse of a composited llsd object
        which is composited of simple llsd types.
        """
        multi_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<array>\
<array>\
<map>\
<key>content-type</key><string>application/binary</string>\
</map>\
<binary>MTIzNDU2Cg==</binary>\
</array>\
<array>\
<map>\
<key>content-type</key><string>application/exe</string>\
</map>\
<binary>d2hpbGUoMSkgeyBwcmludCAneWVzJ307Cg==</binary>\
</array>\
</array>\
</llsd>"

        multi_python = [
            [{'content-type':'application/binary'},b'123456\n'],
            [{'content-type':'application/exe'},b"while(1) { print 'yes'};\n"]]

        self.assertEqual(
            multi_python,
            self.roundTrip(self.llsd.parse(multi_xml)))

    def testInvalidBinaryFormat(self):
        """
        Test the parse with an invalid binary format. LLSDParseError should
        be raised.

        Maps to test scenarios : module:llsd:test#78
        """
        invalid_binary = b"""<?llsd/binary?>\n[\\xx0{}]]"""

        self.assertRaises(llsd.LLSDParseError, llsd.parse, invalid_binary)

    def testParseBinaryIncorrectMIME(self):
        """
        Test parse with binary format data but has an incorrect MIME type.

        LLSDParseError should be raised.

        Maps to test scenarios : module:llsd:test#81
        """
        binary_data = b"""<?llsd/binary?>\n[\x00\x00\x00\x02i\x00\x00\x00{i\x00\x00\x00{]"""

        try:
            llsd.parse(binary_data, llsd.XML_MIME_TYPE)
            self.fail("LLSDParseError should be raised.")
        except llsd.LLSDParseError:
            pass

    def testParseBinaryInvlaidBinaryFormat(self):
        """
        Test the parse_binary with an invalid binary format. LLSDParseError
        should be raised.

        Maps to test scenario : module:llsd:test#82
        """
        invalid_binary = b"""<?llsd/binary?>\n[\\xx0{}]]"""

        self.assertRaises(llsd.LLSDParseError, llsd.parse_binary, invalid_binary)

    def testAsBinaryWithNonSupportedType(self):
        """
        Test the as_binary with a non-supported python type.

        Maps to test scenario module:llsd:test#89
        """
        # make an object not supported by llsd
        python_native_obj = Foo()

        # assert than an exception is raised
        self.assertRaises(TypeError, self.llsd.as_binary, python_native_obj)
        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, b'2')

    def testInvlaidBinaryParse1(self):
        """
        Test with invalid binary format of map.
        """
        invalid_binary = b"""<?llsd/binary?>\n{\x00\x00\x00\x01k\x00\x00\x00\x06'kaka'i\x00\x00\x00{{"""

        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, invalid_binary)

    def testInvlaidBinaryParse2(self):
        """
        Test with invalid binary format of array.
        """
        invalid_binary = b"""<?llsd/binary?>\n[\x00\x00\x00\x02i\x00\x00\x00\x01i\x00\x00\x00\x02*"""

        self.assertRaises(llsd.LLSDParseError, self.llsd.parse, invalid_binary)

    def testParseDelimitedString(self):
        """
        Test parse_binary with delimited string.
        """
        delimited_string = b"""<?llsd/binary?>\n'\\t\\a\\b\\f\\n\\r\\t\\v\\x0f\\p'"""

        self.assertEqual('\t\x07\x08\x0c\n\r\t\x0b\x0fp', llsd.parse(delimited_string))



class LLSDPythonXMLUnitTest(unittest.TestCase):
    """
    This class aggregates all the tests for parse_xml(something), LLSD.as_xml(something)
    and format_xml (i.e. same as LLSD.as_xml(something).
    Note that test scenarios for the same input type are all put into single test method. And utility
    method assert_xml_roundtrip is used to test parse_xml and as_xml at the same time.

    NOTE: Tests in this class use the pure python implementation for
    serialization of llsd object to llsd xml format.
    """
    def setUp(self):
        """
        Create a LLSD object
        """
        self.llsd = llsd.LLSD()

    def assertXMLRoundtrip(self, py, xml, ignore_rounding=False):
        """
        Utility method to test parse_xml and as_xml at the same time
        """

        # use parse to check
        parsed_py = self.llsd.parse(xml)
        parsed_stream = self.llsd.parse(io.BytesIO(xml))
        self.assertEqual(parsed_stream, parsed_py)
        formatted_xml = self.llsd.as_xml(py)
        self.assertEqual(parsed_py, py)
        self.assertEqual(py, self.llsd.parse(formatted_xml))
##      if not ignore_rounding:
##          self.assertEqual(self.strip(formatted_xml),
##                           self.strip(xml))
##          self.assertEqual(self.strip(xml),
##                           self.strip(self.llsd.as_xml(parsed_py)))

        # use parse_xml to check again
        parsed_py = llsd.parse_xml(xml)
        formatted_xml = self.llsd.as_xml(py)
        self.assertEqual(parsed_py, py)
        self.assertEqual(py, llsd.parse_xml(formatted_xml))
##      if not ignore_rounding:
##          self.assertEqual(self.strip(formatted_xml),
##                           self.strip(xml))
##          self.assertEqual(self.strip(xml),
##                           self.strip(self.llsd.as_xml(parsed_py)))

    def testBytesConversion(self):
        """
        Test the __bytes__() conversion on the LLSD class
        """
        if PY2:
            return # not applicable on python 2
        some_xml =b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<integer>1234</integer>\
</llsd>"

        c = llsd.LLSD(llsd.parse_xml(some_xml))
        out_xml = bytes(c)

        self.assertEqual(some_xml, out_xml)

    def testStrConversion(self):
        """
        Test the __str__() conversion on the LLSD class
        """
        some_xml =b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<integer>1234</integer>\
</llsd>"

        c = llsd.LLSD(llsd.parse_xml(some_xml))
        out_xml = str(c).encode()

        self.assertEqual(some_xml, out_xml)

    def testInteger(self):
        """
        Test the parse and serializatioin of input type : integer
        Maps to the test scenarios : module:llsd:test#39 - 41
        """
        pos_int_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<integer>289343</integer>\
</llsd>"

        neg_int_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<integer>-289343</integer>\
</llsd>"

        blank_int_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<integer />\
</llsd>"

        python_pos_int = 289343
        python_neg_int = -289343
        python_blank_int = 0

        self.assertXMLRoundtrip(python_pos_int,
                                  pos_int_xml)
        self.assertXMLRoundtrip(python_neg_int,
                                  neg_int_xml)
        self.assertEqual(python_blank_int, self.llsd.parse(blank_int_xml))

    def testUndefined(self):
        """
        Test the parse and serialization of input type: undef

        Maps to test scenarios module:llsd:test#42
        """
        undef_xml = b"<?xml version=\"1.0\" ?><llsd><undef /></llsd>"
        self.assertXMLRoundtrip(None, undef_xml)

    def testBoolean(self):
        """
        Test the parse and serialization of input tye: boolean. -> llsd:test 43 - 45
        """
        true_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<boolean>true</boolean>\
</llsd>"

        false_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<boolean>false</boolean>\
</llsd>"

        blank_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<boolean />\
</llsd>"

        self.assertXMLRoundtrip(True, true_xml)
        self.assertXMLRoundtrip(False, false_xml)
        self.assertEqual(False, self.llsd.parse(blank_xml))

    def testReal(self):
        """
        Test the parse and serialization of input type : real.
        Maps to test scenarios module:llsd:test# 46 - 48
        """
        pos_real_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<real>2983287453.3000002</real>\
</llsd>"

        neg_real_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<real>-2983287453.3000002</real>\
</llsd>"

        blank_real_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<real />\
</llsd>"

        python_pos_real = 2983287453.3
        python_neg_real = -2983287453.3
        python_blank_real = 0.0

        self.assertXMLRoundtrip(python_pos_real,
                                  pos_real_xml, True)
        self.assertXMLRoundtrip(python_neg_real,
                                  neg_real_xml, True)
        self.assertEqual(python_blank_real, self.llsd.parse(blank_real_xml))

    def testUUID(self):
        """
        Test the parse and serialization of input type: UUID.
        Maps to test scenarios module:llsd:test#49
        """
        uuid_tests = {
            uuid.UUID(hex='d7f4aeca-88f1-42a1-b385-b9db18abb255'):b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<uuid>d7f4aeca-88f1-42a1-b385-b9db18abb255</uuid>\
</llsd>",
            uuid.UUID(int=0):b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<uuid />\
</llsd>"}

        for py, xml in uuid_tests.items():
            self.assertXMLRoundtrip(py, xml)


    def testString(self):
        """
        Test the parse and serialization of input type : String.
        Maps to test scenarios module:llsd:test# 50 - 51
        """
        sample_data = {'foo':b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<string>foo</string>\
</llsd>",
            '':b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<string />\
</llsd>",
            '<xml>&ent;</xml>':b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<string>&lt;xml&gt;&amp;ent;&lt;/xml&gt;</string>\
</llsd>"
            }
        for py, xml in sample_data.items():
            self.assertXMLRoundtrip(py, xml)

    def testURI(self):
        """
        Test the parse and serialization of input type: URI.
        Maps to test scenarios module:llsd:test# 52 - 53
        """
        uri_tests = {
            llsd.uri('http://sim956.agni.lindenlab.com:12035/runtime/agents'):b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<uri>http://sim956.agni.lindenlab.com:12035/runtime/agents</uri>\
</llsd>"}

        blank_uri_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<uri />\
</llsd>"

        for py, xml in uri_tests.items():
            self.assertXMLRoundtrip(py, xml)
        self.assertEqual('', self.llsd.parse(blank_uri_xml))

    def testDate(self):
        """
        Test the parse and serialization of input type : Date.
        Maps to test scenarios module:llsd:test#54 - 57
        """
        valid_date_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<date>2006-02-01T14:29:53.460000Z</date>\
</llsd>"

        valid_date_xml_no_fractional = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<date>2006-02-01T14:29:53Z</date>\
</llsd>"
        valid_date_xml_filled = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<date>2006-02-01T14:29:05Z</date>\
</llsd>"

        blank_date_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<date />\
</llsd>"

        before_19th_century_date = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<date>1853-02-01T00:00:00Z</date>\
</llsd>"

        python_valid_date = datetime(2006, 2, 1, 14, 29, 53, 460000)
        python_valid_date_no_fractional = datetime(2006, 2, 1, 14, 29, 53)
        python_valid_date_filled = datetime(2006, 2, 1, 14, 29, 5)
        python_blank_date = datetime(1970, 1, 1)
        python_19th_century_date = datetime(1853, 2, 1)
        self.assertXMLRoundtrip(python_valid_date,
                                  valid_date_xml)
        self.assertXMLRoundtrip(python_valid_date_no_fractional,
                                  valid_date_xml_no_fractional)
        self.assertXMLRoundtrip(python_valid_date_filled,
                                  valid_date_xml_filled)
        self.assertXMLRoundtrip(python_19th_century_date,
                                before_19th_century_date)
        self.assertEqual(python_blank_date, self.llsd.parse(blank_date_xml))

    def testArray(self):
        """
        Test the parse and serialization of input type : Array.
        Maps to test scenarios module:llsd:test# 58 - 60
        """
        # simple array
        array_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<array>\
<string>foo</string>\
<string>bar</string>\
</array>\
</llsd>"
        # composite array
        array_within_array_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<array>\
<string>foo</string>\
<string>bar</string>\
<array>\
<string>foo</string>\
<string>bar</string>\
</array>\
</array>\
</llsd>"
        # blank array
        blank_array_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<array />\
</llsd>"

        python_array = ["foo", "bar"]
        python_array_within_array = ["foo", "bar", ["foo", "bar"]]

        self.assertXMLRoundtrip(python_array, array_xml)
        self.assertXMLRoundtrip(python_array_within_array,
                                  array_within_array_xml)
        self.assertXMLRoundtrip([], blank_array_xml)

    def testMap(self):
        """
        Test the parse and serialization of input type : map.
        Maps to test scenarios module:llsd:test# 61 - 63
        """
        # simple map
        map_xml = b"""\
<?xml version="1.0" ?>
<llsd>
<map>
<key>foo</key>
<string>bar</string>
</map>
</llsd>"""
        # composite map
        map_within_map_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<map>\
<key>foo</key>\
<string>bar</string>\
<key>doo</key>\
<map>\
<key>goo</key>\
<string>poo</string>\
</map>\
</map>\
</llsd>"
        # blank map
        blank_map_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<map />\
</llsd>"

        python_map = {"foo":"bar"}
        python_map_within_map = {"foo":"bar", "doo":{"goo":"poo"}}

        self.assertXMLRoundtrip(python_map, map_xml)
        self.assertXMLRoundtrip(python_map_within_map,
                                  map_within_map_xml)
        self.assertXMLRoundtrip({}, blank_map_xml)

    def testDeepMap(self):
        """
        Test that formatting a deeply nested map does not cause a RecursionError
        """

        test_map = {"foo":"bar", "depth":0, "next":None}
        max_depth = 200
        for depth in range(max_depth):
            test_map = {"foo":"bar", "depth":depth, "next":test_map}

        # this should not throw an exception.
        test_xml = self.llsd.as_xml(test_map)


    def testBinary(self):
        """
        Test the parse and serialization of input type : binary.
        Maps to test scenarios module:llsd:test#64
        """
        base64_binary_xml = b"\
<?xml version=\"1.0\" ?>\
<llsd>\
<binary>dGhlIHF1aWNrIGJyb3duIGZveA==</binary>\
</llsd>"

        python_binary = llsd.binary(b"the quick brown fox")
        self.assertXMLRoundtrip(python_binary,
                                  base64_binary_xml)

        blank_binary_xml = b"""<?xml version="1.0" ?><llsd><binary /></llsd>"""

        python_binary = llsd.binary(b'');

        self.assertXMLRoundtrip(python_binary, blank_binary_xml)

    def testXMLOfAllTypes(self):
        """
        Test parse_xml with complex xml data which contains all types xml element.
        Maps to test scenarios module:llsd:test#65
        """
        xml_of_all_types = b"""<?xml version="1.0" encoding="UTF-8"?>
            <llsd>
                <array>
		<string>string1</string>
		<real>3.1415</real>
		<integer>18686</integer>
		<undef/>
		<uri>www.topcoder.com/tc</uri>
		<date>2006-02-01T14:29:53.43Z</date>
			<map>
				<key>region_id</key>
				<uuid>67153d5b-3659-afb4-8510-adda2c034649</uuid>
				<key>scale</key>
				<string>one minute</string>
				<key>simulator statistics</key>
				<map>
					<key>time dilation</key>
					<real>0.9878624</real>
					<key>sim fps</key>
					<real>44.38898</real>
					<key>pysics fps</key>
					<real>44.38906</real>
					<key>agent updates per second</key>
					<real>1.34</real>
					<key>lsl instructions per second</key>
					<real>0</real>
					<key>total task count</key>
					<real>4</real>
					<key>active task count</key>
					<real>0</real>
					<key>active script count</key>
					<real>4</real>
					<key>main agent count</key>
					<real>0</real>
					<key>child agent count</key>
					<real>0</real>
					<key>inbound packets per second</key>
					<real>1.228283</real>
					<key>outbound packets per second</key>
					<real>1.277508</real>
					<key>pending downloads</key>
					<real>0</real>
					<key>pending uploads</key>
					<real>0.0001096525</real>
					<key>frame ms</key>
					<real>0.7757886</real>
					<key>net ms</key>
					<real>0.3152919</real>
					<key>sim other ms</key>
					<real>0.1826937</real>
					<key>sim physics ms</key>
					<real>0.04323055</real>
					<key>agent ms</key>
					<real>0.01599029</real>
					<key>image ms</key>
					<real>0.01865955</real>
					<key>script ms</key>
					<real>0.1338836</real>
				</map>
			</map>
		</array>
	</llsd>"""

        python_object = ['string1', 3.1415, 18686, None,
            'www.topcoder.com/tc', datetime(2006, 2, 1, 14, 29, 53, 430000),
            {'scale': 'one minute', 'region_id':
            uuid.UUID('67153d5b-3659-afb4-8510-adda2c034649'),
            'simulator statistics': {'total task count': 4.0, 'active task count': 0.0,
            'time dilation': 0.9878624, 'lsl instructions per second': 0.0, 'frame ms':
            0.7757886, 'agent ms': 0.01599029, 'sim other ms': 0.1826937,
            'pysics fps': 44.38906, 'outbound packets per second': 1.277508,
            'pending downloads': 0.0, 'pending uploads': 0.0001096525, 'net ms': 0.3152919,
            'agent updates per second': 1.34, 'inbound packets per second':
            1.228283, 'script ms': 0.1338836, 'main agent count': 0.0,
            'active script count': 4.0, 'image ms': 0.01865955, 'sim physics ms':
            0.04323055, 'child agent count': 0.0, 'sim fps': 44.38898}}]

        parsed_python = llsd.parse(xml_of_all_types)

        self.assertEqual(python_object, parsed_python)

    def testFormatPrettyXML(self):
        """
        Test the format_pretty_xml function, characters like \n,\t should be generated within
        the output to beautify the output xml.

        This maps to test scenarios module:llsd:test#75
        """
        python_object = {'id': ['string1', 123, {'name': 123}]}

        output_xml = llsd.format_pretty_xml(python_object)

        # check whether the output_xml contains whitespaces and new line character
        whitespaces_count = output_xml.count(b' ')
        newline_count = output_xml.count(b'\n')

        self.assertTrue(whitespaces_count > 50)
        self.assertTrue(newline_count > 10)

        # remove all the whitespaces and new line chars from output_xml
        result = self.strip(output_xml)

        # the result should equal to the reuslt of format_xml
        # the xml version tag should be removed before comparing
        format_xml_result = self.llsd.as_xml(python_object)
        self.assertEqual(result[result.find(b"?>") + 2: len(result)],
                         format_xml_result[format_xml_result.find(b"?>") + 2: len(format_xml_result)])

    def testLLSDSerializationFailure(self):
        """
        Test serialization function as_xml with an object of non-supported type.
        TypeError should be raised.

        This maps test scenarios module:llsd:test#90
        """
        # make an object not supported by llsd
        python_native_obj = Foo()

        # assert than an exception is raised
        self.assertRaises(TypeError, self.llsd.as_xml, python_native_obj)

    def testParseXMLIncorrectMIME(self):
        """
        Test parse function with llsd in xml format but with incorrect mime type.

        Maps to test scenario module:llsd:test#80
        """
        llsd_xml = b"""<?xml version="1.0" ?><llsd><real>12.3232</real></llsd>"""

        try:
            self.llsd.parse(llsd_xml, llsd.NOTATION_MIME_TYPE)
            self.fail("LLSDParseError should be raised.")
        except llsd.LLSDParseError:
            pass

    def testParseXMLIncorrectMIME2(self):
        """
        Test parse function with llsd in xml format but with incorrect mime type.

        Maps to test scenario module:llsd:test#80
        """
        llsd_xml = b"""<?xml version="1.0" ?><llsd><real>12.3232</real></llsd>"""

        try:
            self.llsd.parse(llsd_xml, llsd.BINARY_MIME_TYPE)
            self.fail("LLSDParseError should be raised.")
        except llsd.LLSDParseError:
            pass

    def testParseMalformedXML(self):
        """
        Test parse with malformed llsd xml. LLSDParseError should be raised.

        Maps to test scenarios module:llsd:test#77
        """
        malformed_xml = b"""<?xml version="1.0" ?><llsd>string>123/llsd>"""
        self.assertRaises(llsd.LLSDParseError, llsd.parse, malformed_xml)

    def testParseXMLUnsupportedTag(self):
        """
        Test parse with llsd xml which has non-supported tag. LLSDParseError
        should be raised.

        Maps to test scenario module:llsd:test#83
        """
        unsupported_tag_xml = b"""<?xml version="1.0" ?><llsd><string>123</string>
                                <lala>1</lala>/llsd>"""
        self.assertRaises(llsd.LLSDParseError, llsd.parse, unsupported_tag_xml)

    def testParseXMLWithoutRootTag(self):
        """
        Test parse with xml which does not have root tag <llsd>.
        LLSDParseError should be raised.

        Maps to test scenario module:llsd:test#84
        """
        no_root_tag_xml = b"""<array><string>test</string><real>1.3434</real></array>"""

        self.assertRaises(llsd.LLSDParseError, llsd.parse, no_root_tag_xml)

    def testParseXMLUnclosedTag(self):
        """
        Test parse with xml which has unclosed tag.
        LLSDParseError should be raised.

        Maps to test scenario module:llsd:test#85
        """
        unclosed_tag_xml = b"""<?xml version="1.0" ?><llsd><string>123</string>
                                <integer>12345/llsd>"""
        self.assertRaises(llsd.LLSDParseError, llsd.parse, unclosed_tag_xml)

    def strip(self, the_string):
        """
        Utility method to remove all the whitespace characters from
        the given string.
        """
        return re.sub(br'\s', b'', the_string)

    def test_segfault(self):
        for i, badstring in enumerate([
            b'<?xml \xee\xae\x94 ?>',
            b'<?xml \xc4\x9d ?>',
            b'<?xml \xc8\x84 ?>',
            b'<?xml \xd9\xb5 ?>',
            b'<?xml \xd9\xaa ?>',
            b'<?xml \xc9\x88 ?>',
            b'<?xml \xcb\x8c ?>']):
            self.assertRaises(llsd.LLSDParseError, llsd.parse, badstring)

class LLSDStressTest(unittest.TestCase):
    """
    This class aggregates all the stress tests for llsd.
    """

    # python object used for testing
    python_object = [{'destination': 'http://secondlife.com'}, {'version':
            1}, {'modification_date': datetime(2006, 2, 1, 14, 29, 53,
                                               460000)}, {'first_name': 'Phoenix', 'last_name': 'Linden', 'granters':
            [uuid.UUID('a2e76fcd-9360-4f6d-a924-000000000003')], 'look_at': [-0.043753,
            -0.999042, 0.0], 'attachment_data': [{'attachment_point':
            2, 'item_id': uuid.UUID('d6852c11-a74e-309a-0462-50533f1ef9b3'),
            'asset_id': uuid.UUID('c69b29b1-8944-58ae-a7c5-2ca7b23e22fb')},
            {'attachment_point': 10, 'item_id':
            uuid.UUID('ff852c22-a74e-309a-0462-50533f1ef900'), 'asset_id':
            uuid.UUID('5868dd20-c25a-47bd-8b4c-dedc99ef9479')}], 'session_id':
            uuid.UUID('2c585cec-038c-40b0-b42e-a25ebab4d132'), 'agent_id':
            uuid.UUID('3c115e51-04f4-523c-9fa6-98aff1034730'), 'circuit_code': 1075,
            'position': [70.9247, 254.378,
            38.7304]}]

    # how many times to run
    number = 5000

    def testParseAndFormatXMLStress(self):
        """
        Stress test for parse_xml and as_xml.

        Maps to test scenraio module:llsd:test#95
        """
        t = time.time()
        for i in range(0, self.number):
            x = llsd.format_xml(self.python_object)
        delta = time.time() - t
        print("format_xml", str(self.number), " times takes total :", delta, "secs")
        print("average time:", delta / self.number, "secs")

        t = time.time()
        for i in range(0, self.number):
            r = llsd.parse(x)
        delta = time.time() - t
        print("parse_xml", str(self.number), " times takes total :", delta, "secs")
        print("average time:", delta / self.number, "secs")


    def testParseAndFormatNotationStress(self):
        """
        Stress test for parse_notation and as_notation.

        Maps to test scenario module:llsd:test#96
        """
        t = time.time()
        for i in range(0, self.number):
            x = llsd.format_notation(self.python_object)
        delta = time.time() - t
        print("format_notation", str(self.number), " times takes total :", delta, "secs")
        print("average time:", delta / self.number, "secs")

        t = time.time()
        for i in range(0, self.number):
            r = llsd.parse(x)
        delta = time.time() - t
        print("parse_notation", str(self.number), " times takes total :", delta, "secs")
        print("average time:", delta / self.number, "secs")

    def testParseAndFormatBinaryStress(self):
        """
        Stress test for parse_binary and as_binary.

        Maps to test scenarios module:llsd:test#97,98
        """
        t = time.time()
        for i in range(0, self.number):
            x = llsd.format_binary(self.python_object)
        delta = time.time() - t
        print("format_binary", str(self.number), " times takes total :", delta, "secs")
        print("average time:", delta / self.number, "secs")

        t = time.time()
        for i in range(0, self.number):
            r = llsd.parse(x)
        delta = time.time() - t
        print("parse_binary", str(self.number), " times takes total :", delta, "secs")
        print("average time:", delta / self.number, "secs")


FUZZ_ITERATIONS = 5000
class LLSDFuzzTest(unittest.TestCase):
    """
    This class aggregates all the fuzz tests for llsd.
    """
    python_object = LLSDStressTest.python_object
    def assertEqualsPretty(self, a, b):
        try:
            self.assertEqual(a,b)
        except AssertionError:
            self.fail("\n%s\n !=\n%s" % (pprint.pformat(a), pprint.pformat(b)))

    def fuzz_parsing_base(self, fuzz_method_name, legit_exceptions):
        fuzzer = LLSDFuzzer(seed=1234)
        fuzz_method = getattr(fuzzer, fuzz_method_name)
        for f in islice(fuzz_method(self.python_object), FUZZ_ITERATIONS):
            try:
                parsed = llsd.parse(f)
            except legit_exceptions:
                pass  # expected, since many of the inputs will be invalid
            except Exception as e:
                print("Raised exception", e.__class__)
                print("Fuzzed value was", repr(f))
                raise

    def fuzz_roundtrip_base(self, formatter_method, normalize=None):
        fuzzer = LLSDFuzzer(seed=1234)
        for f in islice(fuzzer.structure_fuzz(self.python_object), FUZZ_ITERATIONS):
            try:
                try:
                    text = formatter_method(f)
                except llsd.LLSDSerializationError:
                    # sometimes the fuzzer will generate invalid llsd
                    continue
                parsed = llsd.parse(text)
                try:
                    self.assertEqualsPretty(parsed, f)
                except AssertionError:
                    if normalize:
                        self.assertEqualsPretty(normalize(parsed), normalize(f))
                    else:
                        raise
            except llsd.LLSDParseError:
                print("Failed to parse", repr(text))
                raise


    def test_notation_parsing(self):
        self.fuzz_parsing_base('notation_fuzz',
            (llsd.LLSDParseError, IndexError, ValueError))

    def test_notation_roundtrip(self):
        def normalize(s):
            """ Certain transformations of input data are permitted by
            the spec; this function normalizes a python data structure
            so it receives these transformations as well.
            * date objects -> datetime objects (parser only produces datetimes)
            * nan converted to None (just because nan's are incomparable)
            """
            if is_string(s):
                return s
            if isnan(s):
                return None
            if isinstance(s, date):
                return datetime(s.year, s.month, s.day)
            if isinstance(s, (list, tuple)):
                s = [normalize(x) for x in s]
            if isinstance(s, dict):
                s = dict([(normalize(k), normalize(v))
                          for k,v in s.items()])
            return s

        self.fuzz_roundtrip_base(llsd.format_notation, normalize)

    def test_binary_parsing(self):
        self.fuzz_parsing_base('binary_fuzz',
            (llsd.LLSDParseError, IndexError, ValueError))

    def test_binary_roundtrip(self):
        def normalize(s):
            """ Certain transformations of input data are permitted by
            the spec; this function normalizes a python data structure
            so it receives these transformations as well.
            * date objects -> datetime objects (parser only produces datetimes)
            * fractional seconds dropped from datetime objects
            * integral values larger than a signed 32-bit int become wrapped
            * integral values larger than an unsigned 32-bit int become 0
            * nan converted to None (just because nan's are incomparable)
            """
            if isnan(s):
                return None
            if is_integer(s):
                if (s > (2<<30) - 1 or
                    s < -(2<<30)):
                    return struct.unpack('!i', struct.pack('!i', s))[0]
            if isinstance(s, date):
                return datetime(s.year, s.month, s.day)
            if isinstance(s, datetime):
                return datetime(s.year, s.month, s.day, s.hour, s.minute, s.second)
            if isinstance(s, (list, tuple)):
                s = [normalize(x) for x in s]
            if isinstance(s, dict):
                s = dict([(normalize(k), normalize(v))
                          for k,v in s.items()])
            return s
        self.fuzz_roundtrip_base(llsd.format_binary, normalize)

    def test_xml_parsing(self):
        self.fuzz_parsing_base('xml_fuzz',
            (llsd.LLSDParseError, IndexError, ValueError))

    newline_re = re.compile(r'[\r\n]+')

    @pytest.mark.skipif(PY2, reason="Fails because fuzz generates invalid unicode sequences on Python 2")
    def test_xml_roundtrip(self):
        def normalize(s):
            """ Certain transformations of input data are permitted by
            the spec; this function normalizes a python data structure
            so it receives these transformations as well.
            * codepoints disallowed in xml dropped from strings and unicode objects
            * any sequence of \n and \r compressed into a single \n
            * date objects -> datetime objects (parser only produces datetimes)
            * nan converted to None (just because nan's are incomparable)
            """
            if is_string(s):
                s = remove_invalid_xml_bytes(s)
                s = self.newline_re.sub('\n', s)
                if is_unicode(s):
                    s = s.replace(u'\uffff', u'')
                    s = s.replace(u'\ufffe', u'')
                return s
            if isnan(s):
                return None
            if isinstance(s, date):
                return datetime(s.year, s.month, s.day)
            if isinstance(s, (list, tuple)):
                s = [normalize(x) for x in s]
            if isinstance(s, dict):
                s = dict([(normalize(k), normalize(v))
                          for k,v in s.items()])
            return s
        self.fuzz_roundtrip_base(llsd.format_xml, normalize)

class Regression(unittest.TestCase):
    '''
    Regression tests.
    '''

    def test_no_newline_in_base64_notation(self):
        n = llsd.format_notation(llsd.binary(b'\0'*100))
        self.assertEqual(n.replace(b'\n', b''), n)

    def test_no_newline_in_base64_xml(self):
        n = llsd.format_xml(llsd.binary(b'\0'*100))
        self.assertEqual(n.replace(b'\n', b''), n)

    def test_SL_13073(self):
        # "new note" in Russian with Cyrillic characters.
        good_xml = u'<?xml version="1.0" ?><llsd><string>Новая заметка</string></llsd>'.encode('utf8')
        new_note_unicode = u"Новая заметка"
        new_note_str = "Новая заметка"

        # Py2 unicode
        # Py3 str (unicode)
        self.assertEqual(llsd.format_xml(new_note_unicode), good_xml)

        # Py2 LLSD(unicode)
        # Py3 LLSD(str (unicode))
        self.assertEqual(llsd.format_xml(llsd.LLSD(new_note_unicode)), good_xml)

        # Py2 str (b"")
        # Py3 str (unicode)
        self.assertEqual(llsd.format_xml(new_note_str), good_xml)

        # Py2 LLSD(str (b""))
        # Py3 LLSD(str (unicode))
        self.assertEqual(llsd.format_xml(llsd.LLSD(new_note_str)), good_xml)

        if PY2:
            bytes_xml = good_xml
        else:
            bytes_xml = b'<?xml version="1.0" ?><llsd><binary>0J3QvtCy0LDRjyDQt9Cw0LzQtdGC0LrQsA==</binary></llsd>'
        # Py2 str (b"")
        # Py3 bytes (turned into binary type by llsd)
        self.assertEqual(llsd.format_xml(new_note_unicode.encode("utf-8")), bytes_xml)

        # Py2 LLSD(str (b""))
        # Py3 LLSD(bytes) (turned into binary type by llsd)
        self.assertEqual(llsd.format_xml(llsd.LLSD(new_note_unicode.encode("utf-8"))), bytes_xml)

class MapConstraints(unittest.TestCase):
    '''
    Implied type conversion tests
    '''

    def test_int_map_key(self):
        '''
        LLSD Map keys are supposed to be strings; convert a map with an int key
        '''
        llsdmap=llsd.LLSD({5 : 'int'})
        self.assertEqual(llsd.format_xml(llsdmap), b'<?xml version="1.0" ?><llsd><map><key>5</key><string>int</string></map></llsd>')
        self.assertEqual(llsd.format_notation(llsdmap), b"{'5':'int'}")

    def test_date_map_key(self):
        '''
        LLSD Map keys are supposed to be strings; convert a map with a date key
        '''
        llsdmap=llsd.LLSD({datetime(2006, 2, 1, 14, 29, 53, 460000) : 'date'})
        self.assertEqual(llsd.format_xml(llsdmap), b'<?xml version="1.0" ?><llsd><map><key>2006-02-01 14:29:53.460000</key><string>date</string></map></llsd>')
        self.assertEqual(llsd.format_notation(llsdmap), b"{'2006-02-01 14:29:53.460000':'date'}")

    def test_uuid_map_key(self):
        '''
        LLSD Map keys are supposed to be strings; convert a map with a uuid key
        '''
        llsdmap=llsd.LLSD({uuid.UUID(int=0) : 'uuid'})
        self.assertEqual(llsd.format_xml(llsdmap), b'<?xml version="1.0" ?><llsd><map><key>00000000-0000-0000-0000-000000000000</key><string>uuid</string></map></llsd>')
        self.assertEqual(llsd.format_notation(llsdmap), b"{'00000000-0000-0000-0000-000000000000':'uuid'}")
