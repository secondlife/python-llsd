window.BENCHMARK_DATA = {
  "lastUpdate": 1694117688717,
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
          "id": "ed393fde08e3669bbc9d2d9214aa10e1022b2563",
          "message": "Add PyPI trusted publication (#12)\n\nAdd PyPI trusted publication\r\n\r\nPublish llsd with PyPI's new [trusted publisher](https://blog.pypi.org/posts/2023-04-20-introducing-trusted-publishers/) functionality rather than an access token.",
          "timestamp": "2023-04-21T10:39:22-07:00",
          "tree_id": "b9dc9d85eba28f2b9b1ed09b6201cb3b42838560",
          "url": "https://github.com/secondlife/python-llsd/commit/ed393fde08e3669bbc9d2d9214aa10e1022b2563"
        },
        "date": 1682098796079,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 8401.410233480117,
            "unit": "iter/sec",
            "range": "stddev: 0.000028143593606264825",
            "extra": "mean: 119.02763610029906 usec\nrounds: 3108"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 3103.4882017496516,
            "unit": "iter/sec",
            "range": "stddev: 0.0002465618766434401",
            "extra": "mean: 322.2180768840141 usec\nrounds: 1964"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 11845.999955317911,
            "unit": "iter/sec",
            "range": "stddev: 0.00007200932853574851",
            "extra": "mean: 84.41668105452588 usec\nrounds: 5653"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 3598.045609310651,
            "unit": "iter/sec",
            "range": "stddev: 0.00008768229864581673",
            "extra": "mean: 277.9286614411733 usec\nrounds: 3317"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 9989.97967818425,
            "unit": "iter/sec",
            "range": "stddev: 0.00005278396556448257",
            "extra": "mean: 100.10030372571859 usec\nrounds: 2657"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 14149.262982134755,
            "unit": "iter/sec",
            "range": "stddev: 0.000047877897681145966",
            "extra": "mean: 70.67505927783147 usec\nrounds: 8418"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 10445.428648020821,
            "unit": "iter/sec",
            "range": "stddev: 0.000033306463552091626",
            "extra": "mean: 95.73565946376723 usec\nrounds: 4998"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 20189.290617260536,
            "unit": "iter/sec",
            "range": "stddev: 0.00002340255990154317",
            "extra": "mean: 49.53121033113787 usec\nrounds: 8905"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 21068.91781205809,
            "unit": "iter/sec",
            "range": "stddev: 0.000019710617091594125",
            "extra": "mean: 47.46328259098734 usec\nrounds: 10977"
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
          "id": "46fdce0be06eb90cc2bf0bb4d1736cd81844b890",
          "message": "Switch PyPI action param case to kebab\n\nFixes deprecation warning about repository_url.",
          "timestamp": "2023-05-04T12:36:02-07:00",
          "tree_id": "e77533ea846462ef801ec06f8ad47aa995ba4a5e",
          "url": "https://github.com/secondlife/python-llsd/commit/46fdce0be06eb90cc2bf0bb4d1736cd81844b890"
        },
        "date": 1683228996474,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 8596.225166748598,
            "unit": "iter/sec",
            "range": "stddev: 0.00005808476456724832",
            "extra": "mean: 116.33013102869153 usec\nrounds: 3587"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 3215.5453601785107,
            "unit": "iter/sec",
            "range": "stddev: 0.0002668789446984807",
            "extra": "mean: 310.98923759062916 usec\nrounds: 1793"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 12292.815169082878,
            "unit": "iter/sec",
            "range": "stddev: 0.0000753499327366744",
            "extra": "mean: 81.34833121993539 usec\nrounds: 7886"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 3697.3929771043913,
            "unit": "iter/sec",
            "range": "stddev: 0.00014229848015188685",
            "extra": "mean: 270.4608371878146 usec\nrounds: 3243"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 11152.30995060082,
            "unit": "iter/sec",
            "range": "stddev: 0.00007596157896915804",
            "extra": "mean: 89.66752219311533 usec\nrounds: 6511"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 14294.424712368927,
            "unit": "iter/sec",
            "range": "stddev: 0.000058709002444133834",
            "extra": "mean: 69.95734491747 usec\nrounds: 8834"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 11150.297285691477,
            "unit": "iter/sec",
            "range": "stddev: 0.00005536912357994805",
            "extra": "mean: 89.68370747237758 usec\nrounds: 5179"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 21237.79814122248,
            "unit": "iter/sec",
            "range": "stddev: 0.00003803726295527947",
            "extra": "mean: 47.085860471524306 usec\nrounds: 10858"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 21154.097004896656,
            "unit": "iter/sec",
            "range": "stddev: 0.000040814894197669976",
            "extra": "mean: 47.27216669983712 usec\nrounds: 10030"
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
          "id": "a63abbef1ed29c4e750529854b7f2c43fbe360b8",
          "message": "Merge pull request #13 from secondlife/log/deep_map\n\nSL-18330: In XML formatter, avoid adding call stack depth.",
          "timestamp": "2023-05-08T10:13:57-04:00",
          "tree_id": "c9e8fa449ffcd8dd71fb48e9d3daddac89f3c115",
          "url": "https://github.com/secondlife/python-llsd/commit/a63abbef1ed29c4e750529854b7f2c43fbe360b8"
        },
        "date": 1683555267712,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 12385.13965525791,
            "unit": "iter/sec",
            "range": "stddev: 0.000003357671187857512",
            "extra": "mean: 80.74192361452026 usec\nrounds: 4294"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 4316.033655275787,
            "unit": "iter/sec",
            "range": "stddev: 0.00017824729524758487",
            "extra": "mean: 231.69420812500633 usec\nrounds: 2806"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 15655.984973123714,
            "unit": "iter/sec",
            "range": "stddev: 0.000030265184103295064",
            "extra": "mean: 63.87333672820191 usec\nrounds: 9524"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 4713.246069957984,
            "unit": "iter/sec",
            "range": "stddev: 0.00002772524407139972",
            "extra": "mean: 212.16800166109607 usec\nrounds: 3612"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 14963.893650457858,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016281721266114382",
            "extra": "mean: 66.8275265354751 usec\nrounds: 3109"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 17550.267383165712,
            "unit": "iter/sec",
            "range": "stddev: 0.00003116645055969604",
            "extra": "mean: 56.979188873168056 usec\nrounds: 10515"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 17118.960322648418,
            "unit": "iter/sec",
            "range": "stddev: 0.000012240580240138473",
            "extra": "mean: 58.41476241270318 usec\nrounds: 8439"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 26326.55225540916,
            "unit": "iter/sec",
            "range": "stddev: 0.000011888050812629382",
            "extra": "mean: 37.984464896824306 usec\nrounds: 9643"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 25760.089405910738,
            "unit": "iter/sec",
            "range": "stddev: 0.000001149915234740709",
            "extra": "mean: 38.81974104369944 usec\nrounds: 11249"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "roxanne@roxiware.com",
            "name": "Roxanne Skelly",
            "username": "roxanneskelly"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b703873ef2f5e09155b5d6e58e841145437a3c27",
          "message": "Merge pull request #15 from secondlife/SRV-439\n\nSRV-439 - performance optimizations for string handling in xml formatting",
          "timestamp": "2023-09-07T13:13:19-07:00",
          "tree_id": "90faa284611ea2757c433e5d983d07c90b32965f",
          "url": "https://github.com/secondlife/python-llsd/commit/b703873ef2f5e09155b5d6e58e841145437a3c27"
        },
        "date": 1694117688208,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 12400.876930837765,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020154217057357803",
            "extra": "mean: 80.63945844936653 usec\nrounds: 4308"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 4285.042083926906,
            "unit": "iter/sec",
            "range": "stddev: 0.00002688969382671492",
            "extra": "mean: 233.36993672733738 usec\nrounds: 2750"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 15502.002579149737,
            "unit": "iter/sec",
            "range": "stddev: 0.00003278538982642423",
            "extra": "mean: 64.50779471195575 usec\nrounds: 8510"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 4608.93699067061,
            "unit": "iter/sec",
            "range": "stddev: 0.00002849527827174635",
            "extra": "mean: 216.96977025813015 usec\nrounds: 3517"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 15178.721126042934,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015114742756373176",
            "extra": "mean: 65.88170318804048 usec\nrounds: 7183"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 16951.5580969395,
            "unit": "iter/sec",
            "range": "stddev: 0.00003407958627938856",
            "extra": "mean: 58.99162745285012 usec\nrounds: 10039"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 19329.48894091656,
            "unit": "iter/sec",
            "range": "stddev: 0.00001291174012510934",
            "extra": "mean: 51.73442521199851 usec\nrounds: 7782"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 23281.178240620364,
            "unit": "iter/sec",
            "range": "stddev: 0.000012682945522827392",
            "extra": "mean: 42.95315252796043 usec\nrounds: 10503"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 25350.441553605502,
            "unit": "iter/sec",
            "range": "stddev: 9.170085610769461e-7",
            "extra": "mean: 39.44704465543219 usec\nrounds: 11376"
          },
          {
            "name": "tests/bench.py::test_format_xml_deep",
            "value": 220.80638639515766,
            "unit": "iter/sec",
            "range": "stddev: 0.00006939136434361314",
            "extra": "mean: 4.528854515151516 msec\nrounds: 198"
          },
          {
            "name": "tests/bench.py::test_format_xml_wide",
            "value": 0.5439629781791014,
            "unit": "iter/sec",
            "range": "stddev: 0.004288264931640944",
            "extra": "mean: 1.838360403400003 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_deep",
            "value": 282.30209368668704,
            "unit": "iter/sec",
            "range": "stddev: 0.000037876346844994716",
            "extra": "mean: 3.54230458209017 msec\nrounds: 268"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide",
            "value": 0.6950752910135733,
            "unit": "iter/sec",
            "range": "stddev: 0.004344220335527082",
            "extra": "mean: 1.4386930638000082 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide_array",
            "value": 1.1267186085687908,
            "unit": "iter/sec",
            "range": "stddev: 0.0021471007159548573",
            "extra": "mean: 887.5330471999973 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_deep",
            "value": 250.0105358877701,
            "unit": "iter/sec",
            "range": "stddev: 0.000007938472069168623",
            "extra": "mean: 3.999831432899695 msec\nrounds: 231"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide",
            "value": 0.6229985032994216,
            "unit": "iter/sec",
            "range": "stddev: 0.0011434795723045251",
            "extra": "mean: 1.6051402928000074 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide_array",
            "value": 0.8591906594760393,
            "unit": "iter/sec",
            "range": "stddev: 0.006885452751917601",
            "extra": "mean: 1.1638860234000106 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_parse_xml_deep",
            "value": 257.7893561696026,
            "unit": "iter/sec",
            "range": "stddev: 0.005908778845637322",
            "extra": "mean: 3.8791361088705627 msec\nrounds: 248"
          },
          {
            "name": "tests/bench.py::test_parse_binary_deep",
            "value": 202.06927819673965,
            "unit": "iter/sec",
            "range": "stddev: 0.000034898422119658154",
            "extra": "mean: 4.948797803030579 msec\nrounds: 198"
          }
        ]
      }
    ]
  }
}