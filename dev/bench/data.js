window.BENCHMARK_DATA = {
  "lastUpdate": 1679517446697,
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
      },
      {
        "commit": {
          "author": {
            "email": "nat@lindenlab.com",
            "name": "nat-goodspeed",
            "username": "nat-goodspeed"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c4035fb6ed54bafbb968d778a0e9fa60cb65e74f",
          "message": "Merge pull request #11 from secondlife/signal/bench-readme\n\nAdd basic development instructions",
          "timestamp": "2023-03-16T17:20:51-04:00",
          "tree_id": "a9a8fad2902645e32f4cf61fbcceb95ec10df74a",
          "url": "https://github.com/secondlife/python-llsd/commit/c4035fb6ed54bafbb968d778a0e9fa60cb65e74f"
        },
        "date": 1679001686035,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 8300.473669688761,
            "unit": "iter/sec",
            "range": "stddev: 0.00005706394950755007",
            "extra": "mean: 120.47505236378835 usec\nrounds: 3342"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 2170.2928269190556,
            "unit": "iter/sec",
            "range": "stddev: 0.00029043219624840633",
            "extra": "mean: 460.76731563436005 usec\nrounds: 1695"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 9755.97508852484,
            "unit": "iter/sec",
            "range": "stddev: 0.00006527358784005084",
            "extra": "mean: 102.50128674233892 usec\nrounds: 5280"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 2657.2559583178227,
            "unit": "iter/sec",
            "range": "stddev: 0.0001100800966197872",
            "extra": "mean: 376.32806763299175 usec\nrounds: 1863"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 9057.213634529715,
            "unit": "iter/sec",
            "range": "stddev: 0.000060535948325585013",
            "extra": "mean: 110.40923184008828 usec\nrounds: 5603"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 10356.718680816699,
            "unit": "iter/sec",
            "range": "stddev: 0.00006844433281053462",
            "extra": "mean: 96.55567857146266 usec\nrounds: 6216"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 10817.987785820233,
            "unit": "iter/sec",
            "range": "stddev: 0.00005813904804121425",
            "extra": "mean: 92.43863274746514 usec\nrounds: 2162"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 18440.266312430256,
            "unit": "iter/sec",
            "range": "stddev: 0.000051923028874614916",
            "extra": "mean: 54.229151740933254 usec\nrounds: 10742"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 18598.440988295966,
            "unit": "iter/sec",
            "range": "stddev: 0.00003668074092684782",
            "extra": "mean: 53.76794757309508 usec\nrounds: 9785"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nat@lindenlab.com",
            "name": "nat-goodspeed",
            "username": "nat-goodspeed"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "0adae956ed43a09d71d7200b11eec525a6d7b0d6",
          "message": "Merge pull request #5 from secondlife/sl-19314\n\nSL-19314: Recast llsd serialization to write to a stream.",
          "timestamp": "2023-03-20T14:41:09-04:00",
          "tree_id": "b553a8ff4e2aa4d7c664e0fd49b42f534965f057",
          "url": "https://github.com/secondlife/python-llsd/commit/0adae956ed43a09d71d7200b11eec525a6d7b0d6"
        },
        "date": 1679337702394,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 10141.084204071363,
            "unit": "iter/sec",
            "range": "stddev: 0.00006546413149893282",
            "extra": "mean: 98.60878579417847 usec\nrounds: 3590"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 2451.860006533864,
            "unit": "iter/sec",
            "range": "stddev: 0.0003483534560991509",
            "extra": "mean: 407.8536284025759 usec\nrounds: 1690"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 10133.009280781782,
            "unit": "iter/sec",
            "range": "stddev: 0.0001688658022580344",
            "extra": "mean: 98.68736643679932 usec\nrounds: 6817"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 2854.595266990118,
            "unit": "iter/sec",
            "range": "stddev: 0.0002153905641903825",
            "extra": "mean: 350.3123583100447 usec\nrounds: 2509"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 10584.71309520326,
            "unit": "iter/sec",
            "range": "stddev: 0.00015353939907668615",
            "extra": "mean: 94.4758720435395 usec\nrounds: 930"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 11095.315584964033,
            "unit": "iter/sec",
            "range": "stddev: 0.00016813694472493784",
            "extra": "mean: 90.12812590523909 usec\nrounds: 7593"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 10565.237942231777,
            "unit": "iter/sec",
            "range": "stddev: 0.00008288246169716064",
            "extra": "mean: 94.65002165287365 usec\nrounds: 1755"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 20531.269478147016,
            "unit": "iter/sec",
            "range": "stddev: 0.00004856970267587009",
            "extra": "mean: 48.706194279139716 usec\nrounds: 10593"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 19827.7841545781,
            "unit": "iter/sec",
            "range": "stddev: 0.00007648882122992257",
            "extra": "mean: 50.43427910067837 usec\nrounds: 9785"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "nat@lindenlab.com",
            "name": "nat-goodspeed",
            "username": "nat-goodspeed"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "09310464c7c5ec5df260a151ed191d2a72898d9c",
          "message": "Merge pull request #6 from secondlife/sl-18330-perf\n\nSL-18330: Refactor notation parsing to manage a lookahead char.",
          "timestamp": "2023-03-22T16:36:50-04:00",
          "tree_id": "48e9a5ffd5491d9afb542d5dcc3b3b6daa3e7638",
          "url": "https://github.com/secondlife/python-llsd/commit/09310464c7c5ec5df260a151ed191d2a72898d9c"
        },
        "date": 1679517446149,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 12909.923296042954,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015962367173426108",
            "extra": "mean: 77.45979407224766 usec\nrounds: 4521"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 4227.471582622453,
            "unit": "iter/sec",
            "range": "stddev: 0.00017779182856725737",
            "extra": "mean: 236.54801231795955 usec\nrounds: 2192"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 15563.761914953298,
            "unit": "iter/sec",
            "range": "stddev: 0.000042570073606750205",
            "extra": "mean: 64.2518181314007 usec\nrounds: 9001"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 4641.493022455551,
            "unit": "iter/sec",
            "range": "stddev: 0.000029440320878755105",
            "extra": "mean: 215.44791625496327 usec\nrounds: 3642"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 15632.688204563447,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013954437107169295",
            "extra": "mean: 63.96852460142351 usec\nrounds: 7337"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 17080.303553675392,
            "unit": "iter/sec",
            "range": "stddev: 0.00003450061722708274",
            "extra": "mean: 58.54696884381875 usec\nrounds: 10977"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 13383.90740274769,
            "unit": "iter/sec",
            "range": "stddev: 0.000013177191563706168",
            "extra": "mean: 74.71659582721723 usec\nrounds: 6950"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 25066.830254749835,
            "unit": "iter/sec",
            "range": "stddev: 0.000013077455730759876",
            "extra": "mean: 39.893356672430215 usec\nrounds: 13211"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 26214.91177645831,
            "unit": "iter/sec",
            "range": "stddev: 8.712771456782391e-7",
            "extra": "mean: 38.146227938025206 usec\nrounds: 11683"
          }
        ]
      }
    ]
  }
}