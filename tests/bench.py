from tempfile import TemporaryFile
import unittest

import pytest

import llsd

BENCH_DATA_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<llsd>
  <map>
    <key>integer</key>
    <real>5000</real>
    <key>real</key>
    <real>0.096970</real>
    <key>binary</key>
    <binary>ff55ca5cef2f477f92e011c7de95bb11</binary>
    <key>uri</key>
    <uri>https://secondlife.com</uri>
    <key>date</key>
    <date>2006-02-01T14:29:53Z</date>
    <key>children</key>
    <array>
      <map>
        <key>integer</key>
        <real>5000</real>
        <key>real</key>
        <real>0.096970</real>
        <key>binary</key>
        <binary>ff55ca5cef2f477f92e011c7de95bb11</binary>
        <key>string</key>
        <string>AjWwhTHctcuAxhxK</string>
        <key>id</key>
        <binary>ff55ca5cef2f477f92e011c7de95bb11</binary>
        <key>int_32</key>
        <integer>-1147906088</integer>
        <key>bool</key>
        <boolean>1</boolean>
      </map>
      <real>0.156519</real>
      <binary>ff55ca5cef2f477f92e011c7de95bb11</binary>
      <uri>https://secondlife.com</uri>
      <date>2006-02-01T14:29:53Z</date>
    </array>
  </map>
</llsd>"""

_bench_data = llsd.parse_xml(BENCH_DATA_XML)

    
    
BENCH_DATA_BINARY = llsd.format_binary(_bench_data)
BENCH_DATA_NOTATION = llsd.format_notation(_bench_data)

_tc = unittest.TestCase()
_tc.maxDiff = 5000
assertDictEqual =  _tc.assertDictEqual


@pytest.fixture
def xml_stream():
    with TemporaryFile() as f:
        f.write(BENCH_DATA_XML)
        f.seek(0)
        yield f 


@pytest.fixture
def notation_stream():
    with TemporaryFile() as f:
        d = llsd.format_notation(_bench_data)
        f.write(d)
        f.seek(0)
        yield f


@pytest.fixture
def binary_stream():
    with TemporaryFile() as f:
        d = llsd.format_binary(_bench_data)
        f.write(d)
        f.seek(0)
        yield f

def build_deep_xml():
    deep_data = {}
    curr_data = deep_data
    for i in range(250):
        curr_data["curr_data"] = {}
        curr_data["integer"] = 7
        curr_data["string"] = "string"
        curr_data["map"] = { "item1": 2.345, "item2": [1,2,3], "item3": {"item4": llsd.uri("http://foo.bar.com")}}
        curr_data = curr_data["curr_data"]
        
    return deep_data
_deep_bench_data = build_deep_xml()

def build_wide_xml():
    
    wide_xml = b"""
<?xml version="1.0" encoding="UTF-8"?><llsd><map><key>wide_array</key><array>"
"""
    wide_data = {}
    for i in range(100000):
        wide_data["item"+str(i)] = {"item1":2.345, "item2": [1,2,3], "item3": "string", "item4":{"subitem": llsd.uri("http://foo.bar.com")}}
    return wide_data
_wide_bench_data = build_wide_xml()

def bench_stream(parse, stream):
    ret = parse(stream)
    stream.seek(0)
    return ret


def test_parse_xml_stream(benchmark, xml_stream):
    ret = benchmark(bench_stream, llsd.parse_xml, xml_stream)
    assertDictEqual(ret, _bench_data)


def test_parse_notation_stream(benchmark, notation_stream):
    ret = benchmark(bench_stream, llsd.parse_notation, notation_stream)
    assertDictEqual(ret, _bench_data)


def test_parse_binary_stream(benchmark, binary_stream):
    ret = benchmark(bench_stream, llsd.parse_binary, binary_stream)
    assertDictEqual(ret, _bench_data)


def test_parse_notation_bytes(benchmark):
    ret = benchmark(llsd.parse_notation, BENCH_DATA_NOTATION)
    assertDictEqual(ret, _bench_data)


def test_parse_xml_bytes(benchmark):
    res = benchmark(llsd.parse_xml, BENCH_DATA_XML)
    assertDictEqual(res, _bench_data)


def test_parse_binary_bytes(benchmark):
    res = benchmark(llsd.parse_binary, BENCH_DATA_BINARY)
    assertDictEqual(res, _bench_data)


def test_format_xml(benchmark):
    benchmark(llsd.format_xml, _bench_data)


def test_format_notation(benchmark):
    benchmark(llsd.format_notation, _bench_data)


def test_format_binary(benchmark):
    benchmark(llsd.format_binary, _bench_data)

def test_format_xml_deep(benchmark):
    benchmark(llsd.format_xml, _deep_bench_data)

def test_format_xml_wide(benchmark):
    benchmark(llsd.format_xml, _wide_bench_data)
