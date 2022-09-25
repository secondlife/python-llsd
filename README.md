# llsd

[![codecov](https://codecov.io/gh/secondlife/python-llsd/branch/main/graph/badge.svg?token=Y0CD45CTNI)](https://codecov.io/gh/secondlife/python-llsd)

Official python serialization library for [Linden Lab Structured Data (LLSD)][llsd].

# Use

Install **llsd** with pip:
```
pip install llsd
```

Use **llsd** to parse/format your data:
```py
import llsd

data = {"foo": "bar"}

# Format

data_xml = llsd.format_xml(data)
# >>> '<?xml version="1.0" ?><llsd><map><key>foo</key><string>bar</string></map></llsd>'
data_notation = llsd.format_notation(data)
# >>> "{'foo':'bar'}"
data_binary = llsd.format_binary(data)
# >>> '<?llsd/binary?>\n{\x00\x00\x00\x01k\x00\x00\x00\x03foos\x00\x00\x00\x03bar}'

# Parse

data = llsd.parse(data_xml)
# >>> {'foo: 'bar'}
data = llsd.parse(data_notation)
# >>> {'foo: 'bar'}
data = llsd.parse(data_binary)
# >>> {'foo: 'bar'}
```

[llsd]: https://wiki.secondlife.com/wiki/LLSD
[llbase]: https://pypi.org/project/llbase/
