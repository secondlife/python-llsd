window.BENCHMARK_DATA = {
  "lastUpdate": 1678996299225,
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
      }
    ]
  }
}