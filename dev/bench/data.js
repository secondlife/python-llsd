window.BENCHMARK_DATA = {
  "lastUpdate": 1678996962172,
  "repoUrl": "https://github.com/secondlife/python-llsd",
  "entries": {
    "Python Benchmarks": [
      {
        "commit": {
          "author": {
            "email": "signal@lindenlab.com",
            "name": "Signal Linden",
            "username": "bennettgoble"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "8f5fabab741e3427f85be880d28af5cb9dcfc353",
          "message": "Merge pull request #10 from secondlife/signal/bench-summary\n\nPublish benchmarks in job summary",
          "timestamp": "2023-03-16T12:51:09-07:00",
          "tree_id": "f8f2a6eef383b51ca5c29485a3ac2bc7d9609009",
          "url": "https://github.com/secondlife/python-llsd/commit/8f5fabab741e3427f85be880d28af5cb9dcfc353"
        },
        "date": 1678996298253,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 12872.181812208772,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022186791421610883",
            "extra": "mean: 77.68690767337813 usec\nrounds: 4874"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 2205.4076588476173,
            "unit": "iter/sec",
            "range": "stddev: 0.00019966932409915566",
            "extra": "mean: 453.43090924175266 usec\nrounds: 1807"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 12166.264529452834,
            "unit": "iter/sec",
            "range": "stddev: 0.00003357310024603729",
            "extra": "mean: 82.19449754517001 usec\nrounds: 7740"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 4002.991825681371,
            "unit": "iter/sec",
            "range": "stddev: 0.00003568834188397126",
            "extra": "mean: 249.81315065008522 usec\nrounds: 3153"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 13982.993986334646,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017384725864036928",
            "extra": "mean: 71.5154423278222 usec\nrounds: 6667"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 14578.919949218085,
            "unit": "iter/sec",
            "range": "stddev: 0.00003596055356104874",
            "extra": "mean: 68.59218676577159 usec\nrounds: 8765"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 14470.950234925818,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017050134935794276",
            "extra": "mean: 69.10396233596931 usec\nrounds: 7381"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 24882.69811579331,
            "unit": "iter/sec",
            "range": "stddev: 0.000014272846192442663",
            "extra": "mean: 40.18856778900876 usec\nrounds: 2198"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 26489.816812509813,
            "unit": "iter/sec",
            "range": "stddev: 9.922669037536676e-7",
            "extra": "mean: 37.75035543196925 usec\nrounds: 11313"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "signal@lindenlab.com",
            "name": "Signal Linden",
            "username": "bennettgoble"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "438e41d47687af3040be60a73f01f80cb7c5009a",
          "message": "Merge pull request #9 from secondlife/sl-18330-fix\n\nSL-18830: Fix sporadic notation parse failure with very large input.",
          "timestamp": "2023-03-16T13:02:10-07:00",
          "tree_id": "d6af6f478047eb93b3f084e047405efb7302c204",
          "url": "https://github.com/secondlife/python-llsd/commit/438e41d47687af3040be60a73f01f80cb7c5009a"
        },
        "date": 1678996960629,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 12495.159989307285,
            "unit": "iter/sec",
            "range": "stddev: 0.000001796551337468087",
            "extra": "mean: 80.03098806703944 usec\nrounds: 4609"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 3009.6538886291164,
            "unit": "iter/sec",
            "range": "stddev: 0.00021585645151115033",
            "extra": "mean: 332.26411973088886 usec\nrounds: 2230"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 13524.361867793872,
            "unit": "iter/sec",
            "range": "stddev: 0.000031128561715433327",
            "extra": "mean: 73.9406420632194 usec\nrounds: 8278"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 3703.0402892099933,
            "unit": "iter/sec",
            "range": "stddev: 0.00003487006193489698",
            "extra": "mean: 270.0483715810016 usec\nrounds: 2998"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 13713.750342074072,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020156423101261827",
            "extra": "mean: 72.91951326632942 usec\nrounds: 6671"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 14466.237302542444,
            "unit": "iter/sec",
            "range": "stddev: 0.00003324372179853647",
            "extra": "mean: 69.12647560566766 usec\nrounds: 8547"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 15020.580807426615,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012655967514258396",
            "extra": "mean: 66.57532174159142 usec\nrounds: 7189"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 25999.305531143098,
            "unit": "iter/sec",
            "range": "stddev: 0.000013443974619298474",
            "extra": "mean: 38.462565809773515 usec\nrounds: 12331"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 26090.624414662354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010597874351514089",
            "extra": "mean: 38.3279443261627 usec\nrounds: 11262"
          }
        ]
      }
    ]
  }
}