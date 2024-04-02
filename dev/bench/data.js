window.BENCHMARK_DATA = {
  "lastUpdate": 1712039823734,
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
          "id": "9655ab4629c37881b223060972a1155d4c4f58e0",
          "message": "Merge pull request #16 from secondlife/dependabot/github_actions/actions/checkout-4\n\nBump actions/checkout from 3 to 4",
          "timestamp": "2023-10-05T17:21:08-04:00",
          "tree_id": "5784caaeff5a07eb18d6fe83495cfacf54e70c3c",
          "url": "https://github.com/secondlife/python-llsd/commit/9655ab4629c37881b223060972a1155d4c4f58e0"
        },
        "date": 1696540958005,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 11892.318545601172,
            "unit": "iter/sec",
            "range": "stddev: 0.000001939030663054047",
            "extra": "mean: 84.08789221088331 usec\nrounds: 3980"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 4015.1881579431906,
            "unit": "iter/sec",
            "range": "stddev: 0.00005715691360910909",
            "extra": "mean: 249.0543308715717 usec\nrounds: 2708"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 14850.95786138028,
            "unit": "iter/sec",
            "range": "stddev: 0.00003053199286817588",
            "extra": "mean: 67.33572402090553 usec\nrounds: 8555"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 4299.189034759652,
            "unit": "iter/sec",
            "range": "stddev: 0.00002782497891442754",
            "extra": "mean: 232.60200747509245 usec\nrounds: 3077"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 14303.536946792752,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036565118611130075",
            "extra": "mean: 69.91277777796265 usec\nrounds: 6579"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 16287.337742606274,
            "unit": "iter/sec",
            "range": "stddev: 0.000031853820678365714",
            "extra": "mean: 61.39738831497833 usec\nrounds: 8130"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 18583.04347717172,
            "unit": "iter/sec",
            "range": "stddev: 0.000013046413893901367",
            "extra": "mean: 53.81249854085779 usec\nrounds: 8224"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 22648.759081649958,
            "unit": "iter/sec",
            "range": "stddev: 0.000012418730168823472",
            "extra": "mean: 44.15252934586605 usec\nrounds: 9814"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 23782.58906357611,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024632024686721427",
            "extra": "mean: 42.047566702127305 usec\nrounds: 11274"
          },
          {
            "name": "tests/bench.py::test_format_xml_deep",
            "value": 208.88704459288252,
            "unit": "iter/sec",
            "range": "stddev: 0.00010163733616835158",
            "extra": "mean: 4.787276309782562 msec\nrounds: 184"
          },
          {
            "name": "tests/bench.py::test_format_xml_wide",
            "value": 0.5155495379202011,
            "unit": "iter/sec",
            "range": "stddev: 0.007611663073909226",
            "extra": "mean: 1.9396778126000072 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_deep",
            "value": 265.2713558123921,
            "unit": "iter/sec",
            "range": "stddev: 0.000060017055098687275",
            "extra": "mean: 3.7697247670691976 msec\nrounds: 249"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide",
            "value": 0.662776814607169,
            "unit": "iter/sec",
            "range": "stddev: 0.0010740100628152446",
            "extra": "mean: 1.508803533799994 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide_array",
            "value": 1.093607756147928,
            "unit": "iter/sec",
            "range": "stddev: 0.0014775191073895769",
            "extra": "mean: 914.4046339999932 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_deep",
            "value": 230.31163847318945,
            "unit": "iter/sec",
            "range": "stddev: 0.000009700978028588764",
            "extra": "mean: 4.3419429718329665 msec\nrounds: 213"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide",
            "value": 0.5639411660726928,
            "unit": "iter/sec",
            "range": "stddev: 0.007065359177845713",
            "extra": "mean: 1.7732346212000039 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide_array",
            "value": 0.7780793318289493,
            "unit": "iter/sec",
            "range": "stddev: 0.0014327402783182118",
            "extra": "mean: 1.2852159915999892 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_parse_xml_deep",
            "value": 278.1522972143162,
            "unit": "iter/sec",
            "range": "stddev: 0.000026585225235979346",
            "extra": "mean: 3.595152763485899 msec\nrounds: 241"
          },
          {
            "name": "tests/bench.py::test_parse_binary_deep",
            "value": 193.76847420924514,
            "unit": "iter/sec",
            "range": "stddev: 0.000037005842480491656",
            "extra": "mean: 5.160798236560031 msec\nrounds: 186"
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
          "id": "6a83d7ffcf81b9be5ddb0ba32dfc529864901cc2",
          "message": "Merge pull request #18 from secondlife/dependabot/github_actions/actions/setup-python-5\n\nBump actions/setup-python from 4 to 5",
          "timestamp": "2024-01-02T17:03:40-05:00",
          "tree_id": "3669117e04cb342e077caa8ea8a11a34cbf60f5a",
          "url": "https://github.com/secondlife/python-llsd/commit/6a83d7ffcf81b9be5ddb0ba32dfc529864901cc2"
        },
        "date": 1704233093113,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 15817.748850333048,
            "unit": "iter/sec",
            "range": "stddev: 0.0000049454232572506185",
            "extra": "mean: 63.220121236085035 usec\nrounds: 5015"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 5226.305717036576,
            "unit": "iter/sec",
            "range": "stddev: 0.000023195145688932988",
            "extra": "mean: 191.33974438966055 usec\nrounds: 3654"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 19108.36290998745,
            "unit": "iter/sec",
            "range": "stddev: 0.000027932258397521702",
            "extra": "mean: 52.33310696005914 usec\nrounds: 3908"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 5589.144603128502,
            "unit": "iter/sec",
            "range": "stddev: 0.000024681583520059786",
            "extra": "mean: 178.91825511908456 usec\nrounds: 4786"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 18952.307873543115,
            "unit": "iter/sec",
            "range": "stddev: 0.0000064658372761547725",
            "extra": "mean: 52.76402254925225 usec\nrounds: 9446"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 21056.190666146376,
            "unit": "iter/sec",
            "range": "stddev: 0.000029203695454950567",
            "extra": "mean: 47.49197116683481 usec\nrounds: 14081"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 24611.46043207338,
            "unit": "iter/sec",
            "range": "stddev: 0.000010356354415810582",
            "extra": "mean: 40.63147746798524 usec\nrounds: 11406"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 29878.910875172453,
            "unit": "iter/sec",
            "range": "stddev: 0.000010185781869046188",
            "extra": "mean: 33.46842206457193 usec\nrounds: 14095"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 31830.31941075389,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016043977631718027",
            "extra": "mean: 31.41658703123631 usec\nrounds: 13679"
          },
          {
            "name": "tests/bench.py::test_format_xml_deep",
            "value": 281.1184958242179,
            "unit": "iter/sec",
            "range": "stddev: 0.0003743238945038085",
            "extra": "mean: 3.5572188057853555 msec\nrounds: 242"
          },
          {
            "name": "tests/bench.py::test_format_xml_wide",
            "value": 0.7273139787231522,
            "unit": "iter/sec",
            "range": "stddev: 0.015157278237429421",
            "extra": "mean: 1.3749220133999984 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_deep",
            "value": 355.27013357330435,
            "unit": "iter/sec",
            "range": "stddev: 0.00010387737303301474",
            "extra": "mean: 2.81475954632608 msec\nrounds: 313"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide",
            "value": 0.9181573879351806,
            "unit": "iter/sec",
            "range": "stddev: 0.005372596694519276",
            "extra": "mean: 1.089137889799997 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide_array",
            "value": 1.5495171175811437,
            "unit": "iter/sec",
            "range": "stddev: 0.0068435045283850165",
            "extra": "mean: 645.3623445999995 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_deep",
            "value": 307.0209478293415,
            "unit": "iter/sec",
            "range": "stddev: 0.00009111088945665466",
            "extra": "mean: 3.257106744898244 msec\nrounds: 294"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide",
            "value": 0.7866670063368922,
            "unit": "iter/sec",
            "range": "stddev: 0.013415616560735342",
            "extra": "mean: 1.2711858918000019 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide_array",
            "value": 1.0968526390904527,
            "unit": "iter/sec",
            "range": "stddev: 0.008067776856191717",
            "extra": "mean: 911.6994976000001 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_parse_xml_deep",
            "value": 303.20488262798125,
            "unit": "iter/sec",
            "range": "stddev: 0.006690864989110339",
            "extra": "mean: 3.298099922839814 msec\nrounds: 324"
          },
          {
            "name": "tests/bench.py::test_parse_binary_deep",
            "value": 251.09686230482555,
            "unit": "iter/sec",
            "range": "stddev: 0.000036038591848352536",
            "extra": "mean: 3.982526865612618 msec\nrounds: 253"
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
          "id": "1b60fb99c5e343344cdd6436e63a74a0b6a46b4e",
          "message": "Merge pull request #19 from secondlife/dependabot/github_actions/actions/download-artifact-4\n\nBump actions/download-artifact from 3 to 4",
          "timestamp": "2024-01-02T17:04:14-05:00",
          "tree_id": "79810cd2ef7929fef9a6bd62bfc0f003f88f5f09",
          "url": "https://github.com/secondlife/python-llsd/commit/1b60fb99c5e343344cdd6436e63a74a0b6a46b4e"
        },
        "date": 1704233127821,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 15771.481761552666,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035281675703742757",
            "extra": "mean: 63.40558326217488 usec\nrounds: 4672"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 5301.90037250154,
            "unit": "iter/sec",
            "range": "stddev: 0.000023734886571667883",
            "extra": "mean: 188.61161654159497 usec\nrounds: 3591"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 19579.96773007318,
            "unit": "iter/sec",
            "range": "stddev: 0.000028930327560053272",
            "extra": "mean: 51.07260715573521 usec\nrounds: 11124"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 5648.875129816638,
            "unit": "iter/sec",
            "range": "stddev: 0.000024969177491298888",
            "extra": "mean: 177.02639499352148 usec\nrounds: 2357"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 19468.970623761248,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028126786056716277",
            "extra": "mean: 51.363783906455346 usec\nrounds: 8612"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 21415.164843480532,
            "unit": "iter/sec",
            "range": "stddev: 0.000029627572069086895",
            "extra": "mean: 46.69588150774531 usec\nrounds: 14406"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 24692.406232870944,
            "unit": "iter/sec",
            "range": "stddev: 0.00001093615219869209",
            "extra": "mean: 40.4982807495198 usec\nrounds: 10675"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 30427.164021387784,
            "unit": "iter/sec",
            "range": "stddev: 0.000010198318836456697",
            "extra": "mean: 32.86536988123778 usec\nrounds: 14164"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 32288.153137201123,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021872234414808735",
            "extra": "mean: 30.97111178055706 usec\nrounds: 15101"
          },
          {
            "name": "tests/bench.py::test_format_xml_deep",
            "value": 284.3052779648135,
            "unit": "iter/sec",
            "range": "stddev: 0.00002119795391927093",
            "extra": "mean: 3.5173458866414817 msec\nrounds: 247"
          },
          {
            "name": "tests/bench.py::test_format_xml_wide",
            "value": 0.7247622618050542,
            "unit": "iter/sec",
            "range": "stddev: 0.016197633655692253",
            "extra": "mean: 1.3797627894000073 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_deep",
            "value": 361.24198902906744,
            "unit": "iter/sec",
            "range": "stddev: 0.000053709243070328815",
            "extra": "mean: 2.768227477342161 msec\nrounds: 331"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide",
            "value": 0.9209113636788201,
            "unit": "iter/sec",
            "range": "stddev: 0.006243087274787177",
            "extra": "mean: 1.085880834400001 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide_array",
            "value": 1.5534795298378319,
            "unit": "iter/sec",
            "range": "stddev: 0.004737098711267636",
            "extra": "mean: 643.716238799999 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_deep",
            "value": 310.5755518782681,
            "unit": "iter/sec",
            "range": "stddev: 0.00002613502073306418",
            "extra": "mean: 3.219828457044668 msec\nrounds: 291"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide",
            "value": 0.8077209945185349,
            "unit": "iter/sec",
            "range": "stddev: 0.01187644725045888",
            "extra": "mean: 1.2380512662000058 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide_array",
            "value": 1.080027477964048,
            "unit": "iter/sec",
            "range": "stddev: 0.001494319381775762",
            "extra": "mean: 925.9023686000035 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_parse_xml_deep",
            "value": 356.75666209532955,
            "unit": "iter/sec",
            "range": "stddev: 0.0037188877925861496",
            "extra": "mean: 2.803031046783335 msec\nrounds: 342"
          },
          {
            "name": "tests/bench.py::test_parse_binary_deep",
            "value": 255.45211473630428,
            "unit": "iter/sec",
            "range": "stddev: 0.00004148517106775961",
            "extra": "mean: 3.914627996062083 msec\nrounds: 254"
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
          "id": "5b63d1cd920b7467b1923fbe655e2bfd649bdf89",
          "message": "Merge pull request #20 from secondlife/dependabot/github_actions/actions/upload-artifact-4\n\nBump actions/upload-artifact from 3 to 4",
          "timestamp": "2024-01-02T17:04:54-05:00",
          "tree_id": "6bedc0fbf3e18822694ca41b607b30d3739af50a",
          "url": "https://github.com/secondlife/python-llsd/commit/5b63d1cd920b7467b1923fbe655e2bfd649bdf89"
        },
        "date": 1704233173729,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 15769.089493607331,
            "unit": "iter/sec",
            "range": "stddev: 0.000003844633524595741",
            "extra": "mean: 63.41520227945896 usec\nrounds: 5616"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 5339.77006960269,
            "unit": "iter/sec",
            "range": "stddev: 0.00002338108387787813",
            "extra": "mean: 187.27398126983508 usec\nrounds: 3684"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 19235.995523144546,
            "unit": "iter/sec",
            "range": "stddev: 0.000027955748351179218",
            "extra": "mean: 51.98587194495916 usec\nrounds: 8020"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 5746.025245985933,
            "unit": "iter/sec",
            "range": "stddev: 0.000025343188618617877",
            "extra": "mean: 174.03334604187157 usec\nrounds: 4800"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 19347.75999133648,
            "unit": "iter/sec",
            "range": "stddev: 0.000002971922739142828",
            "extra": "mean: 51.68556982553944 usec\nrounds: 4010"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 21285.335754157324,
            "unit": "iter/sec",
            "range": "stddev: 0.000029437407713210442",
            "extra": "mean: 46.98070124661698 usec\nrounds: 16927"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 25531.57909239875,
            "unit": "iter/sec",
            "range": "stddev: 0.000010580367957196139",
            "extra": "mean: 39.16718180183847 usec\nrounds: 11573"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 30416.006564151143,
            "unit": "iter/sec",
            "range": "stddev: 0.000009935038166048219",
            "extra": "mean: 32.877425834679364 usec\nrounds: 14043"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 32054.371901507402,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026487228024801767",
            "extra": "mean: 31.196992506129046 usec\nrounds: 14546"
          },
          {
            "name": "tests/bench.py::test_format_xml_deep",
            "value": 285.6737382535751,
            "unit": "iter/sec",
            "range": "stddev: 0.00003629488954449132",
            "extra": "mean: 3.5004967768943507 msec\nrounds: 251"
          },
          {
            "name": "tests/bench.py::test_format_xml_wide",
            "value": 0.7402543352994372,
            "unit": "iter/sec",
            "range": "stddev: 0.014458880435002406",
            "extra": "mean: 1.3508870564000062 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_deep",
            "value": 369.97786979043366,
            "unit": "iter/sec",
            "range": "stddev: 0.00009672905832438023",
            "extra": "mean: 2.70286436474276 msec\nrounds: 329"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide",
            "value": 0.9329679625787793,
            "unit": "iter/sec",
            "range": "stddev: 0.011084448751030202",
            "extra": "mean: 1.071848166399991 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide_array",
            "value": 1.5406054815501788,
            "unit": "iter/sec",
            "range": "stddev: 0.00297824455968108",
            "extra": "mean: 649.0954445999932 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_deep",
            "value": 314.42037649064304,
            "unit": "iter/sec",
            "range": "stddev: 0.00003219010147908321",
            "extra": "mean: 3.1804554499977185 msec\nrounds: 300"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide",
            "value": 0.8083644073987081,
            "unit": "iter/sec",
            "range": "stddev: 0.022438961657121583",
            "extra": "mean: 1.2370658466000122 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide_array",
            "value": 1.0711350563990751,
            "unit": "iter/sec",
            "range": "stddev: 0.008000223907686208",
            "extra": "mean: 933.5890876000121 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_parse_xml_deep",
            "value": 308.31658465320214,
            "unit": "iter/sec",
            "range": "stddev: 0.00649825421827752",
            "extra": "mean: 3.2434194259280957 msec\nrounds: 324"
          },
          {
            "name": "tests/bench.py::test_parse_binary_deep",
            "value": 259.7446542997554,
            "unit": "iter/sec",
            "range": "stddev: 0.00005898358736048852",
            "extra": "mean: 3.849934862743937 msec\nrounds: 255"
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
          "id": "c806ece709dc7327f54e12cd0a85746b734bec4a",
          "message": "Merge pull request #22 from secondlife/signal/codecov\n\nBump codecov-action to v4",
          "timestamp": "2024-02-01T08:48:42-08:00",
          "tree_id": "c78813db2067ffe9dc2b99a1a098ae8a7a7dde1b",
          "url": "https://github.com/secondlife/python-llsd/commit/c806ece709dc7327f54e12cd0a85746b734bec4a"
        },
        "date": 1706806195146,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 15347.358820702611,
            "unit": "iter/sec",
            "range": "stddev: 0.000005450338281102883",
            "extra": "mean: 65.15779110155836 usec\nrounds: 4203"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 5288.741300860378,
            "unit": "iter/sec",
            "range": "stddev: 0.000023388532612794963",
            "extra": "mean: 189.08090661143115 usec\nrounds: 3373"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 19293.6063103556,
            "unit": "iter/sec",
            "range": "stddev: 0.000027867923674971253",
            "extra": "mean: 51.830641919093296 usec\nrounds: 11193"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 5651.18047323247,
            "unit": "iter/sec",
            "range": "stddev: 0.000025264927663956554",
            "extra": "mean: 176.9541788192089 usec\nrounds: 4032"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 19154.890757567064,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030005141038747245",
            "extra": "mean: 52.20598815500704 usec\nrounds: 3799"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 21184.636765771902,
            "unit": "iter/sec",
            "range": "stddev: 0.000030012256734448774",
            "extra": "mean: 47.204019169953575 usec\nrounds: 12624"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 24718.948616065412,
            "unit": "iter/sec",
            "range": "stddev: 0.000010599726805374958",
            "extra": "mean: 40.45479504537167 usec\nrounds: 9607"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 30007.52430801591,
            "unit": "iter/sec",
            "range": "stddev: 0.000010159379950217543",
            "extra": "mean: 33.324975087427326 usec\nrounds: 15133"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 31920.89511089033,
            "unit": "iter/sec",
            "range": "stddev: 0.000001827018336480383",
            "extra": "mean: 31.32744230780777 usec\nrounds: 13364"
          },
          {
            "name": "tests/bench.py::test_format_xml_deep",
            "value": 285.4940421694391,
            "unit": "iter/sec",
            "range": "stddev: 0.00026207913101627413",
            "extra": "mean: 3.502700064775802 msec\nrounds: 247"
          },
          {
            "name": "tests/bench.py::test_format_xml_wide",
            "value": 0.7378949977398735,
            "unit": "iter/sec",
            "range": "stddev: 0.006005235618657384",
            "extra": "mean: 1.3552063681999982 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_deep",
            "value": 354.63107863916923,
            "unit": "iter/sec",
            "range": "stddev: 0.00005461366296289827",
            "extra": "mean: 2.8198318202604065 msec\nrounds: 306"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide",
            "value": 0.9081130541100204,
            "unit": "iter/sec",
            "range": "stddev: 0.0023691583071882875",
            "extra": "mean: 1.101184478600004 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide_array",
            "value": 1.5445717578790732,
            "unit": "iter/sec",
            "range": "stddev: 0.004919848933425914",
            "extra": "mean: 647.4286447999987 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_deep",
            "value": 307.5966753600674,
            "unit": "iter/sec",
            "range": "stddev: 0.000017726619914937687",
            "extra": "mean: 3.2510104305562373 msec\nrounds: 288"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide",
            "value": 0.7960918793705465,
            "unit": "iter/sec",
            "range": "stddev: 0.0059001806846304666",
            "extra": "mean: 1.2561364157999946 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide_array",
            "value": 1.1138691084497798,
            "unit": "iter/sec",
            "range": "stddev: 0.01276072662246532",
            "extra": "mean: 897.7715535999948 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_parse_xml_deep",
            "value": 353.0252910370794,
            "unit": "iter/sec",
            "range": "stddev: 0.003966884895120551",
            "extra": "mean: 2.83265824117674 msec\nrounds: 340"
          },
          {
            "name": "tests/bench.py::test_parse_binary_deep",
            "value": 253.97927621589147,
            "unit": "iter/sec",
            "range": "stddev: 0.000036906851917373934",
            "extra": "mean: 3.937329119522194 msec\nrounds: 251"
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
          "id": "acb55e3d613f131371d4a470f772f0e322f4bcce",
          "message": "Merge pull request #23 from secondlife/signal/fix-array-indent\n\nFix array indentation of pretty xml",
          "timestamp": "2024-04-01T23:35:52-07:00",
          "tree_id": "bd5010d3fc8eb79caa56e9d25cdcf456ee4b3bc1",
          "url": "https://github.com/secondlife/python-llsd/commit/acb55e3d613f131371d4a470f772f0e322f4bcce"
        },
        "date": 1712039822653,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/bench.py::test_parse_xml_stream",
            "value": 15338.036976363388,
            "unit": "iter/sec",
            "range": "stddev: 0.000004331856709993063",
            "extra": "mean: 65.19739139637265 usec\nrounds: 4254"
          },
          {
            "name": "tests/bench.py::test_parse_notation_stream",
            "value": 5332.396264314848,
            "unit": "iter/sec",
            "range": "stddev: 0.0000245948764983066",
            "extra": "mean: 187.53294962194425 usec\nrounds: 3176"
          },
          {
            "name": "tests/bench.py::test_parse_binary_stream",
            "value": 19284.815864952467,
            "unit": "iter/sec",
            "range": "stddev: 0.000027818135030237138",
            "extra": "mean: 51.854267471506645 usec\nrounds: 10188"
          },
          {
            "name": "tests/bench.py::test_parse_notation_bytes",
            "value": 5854.368214946115,
            "unit": "iter/sec",
            "range": "stddev: 0.000025867648343098357",
            "extra": "mean: 170.81262457100237 usec\nrounds: 4371"
          },
          {
            "name": "tests/bench.py::test_parse_xml_bytes",
            "value": 19263.501614767185,
            "unit": "iter/sec",
            "range": "stddev: 0.000005072631884570145",
            "extra": "mean: 51.9116420263599 usec\nrounds: 9199"
          },
          {
            "name": "tests/bench.py::test_parse_binary_bytes",
            "value": 21464.343697156215,
            "unit": "iter/sec",
            "range": "stddev: 0.000029175897140904308",
            "extra": "mean: 46.588892449224474 usec\nrounds: 12078"
          },
          {
            "name": "tests/bench.py::test_format_xml",
            "value": 24926.216480845855,
            "unit": "iter/sec",
            "range": "stddev: 0.00001046848390926289",
            "extra": "mean: 40.118403078478984 usec\nrounds: 10720"
          },
          {
            "name": "tests/bench.py::test_format_notation",
            "value": 29926.614027771157,
            "unit": "iter/sec",
            "range": "stddev: 0.000011045711956936568",
            "extra": "mean: 33.41507325459622 usec\nrounds: 13651"
          },
          {
            "name": "tests/bench.py::test_format_binary",
            "value": 31497.118948059262,
            "unit": "iter/sec",
            "range": "stddev: 0.000001664586674172829",
            "extra": "mean: 31.74893556610886 usec\nrounds: 10988"
          },
          {
            "name": "tests/bench.py::test_format_xml_deep",
            "value": 285.4127173566864,
            "unit": "iter/sec",
            "range": "stddev: 0.000039951208860490064",
            "extra": "mean: 3.5036981157019658 msec\nrounds: 242"
          },
          {
            "name": "tests/bench.py::test_format_xml_wide",
            "value": 0.7331961327654465,
            "unit": "iter/sec",
            "range": "stddev: 0.004417990449218888",
            "extra": "mean: 1.3638915363999957 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_deep",
            "value": 356.5444582953051,
            "unit": "iter/sec",
            "range": "stddev: 0.00011026263356797399",
            "extra": "mean: 2.804699320755556 msec\nrounds: 318"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide",
            "value": 0.9236691727590265,
            "unit": "iter/sec",
            "range": "stddev: 0.007131136617704611",
            "extra": "mean: 1.0826387082000053 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_notation_wide_array",
            "value": 1.5434002125635595,
            "unit": "iter/sec",
            "range": "stddev: 0.010704752604469039",
            "extra": "mean: 647.920087 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_deep",
            "value": 297.09737409990527,
            "unit": "iter/sec",
            "range": "stddev: 0.00003245059419092853",
            "extra": "mean: 3.3658998267138127 msec\nrounds: 277"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide",
            "value": 0.7493606807246287,
            "unit": "iter/sec",
            "range": "stddev: 0.004469532851903014",
            "extra": "mean: 1.3344708705999948 sec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_format_binary_wide_array",
            "value": 1.0724915981351262,
            "unit": "iter/sec",
            "range": "stddev: 0.005393651071731648",
            "extra": "mean: 932.408236800012 msec\nrounds: 5"
          },
          {
            "name": "tests/bench.py::test_parse_xml_deep",
            "value": 332.52609466548023,
            "unit": "iter/sec",
            "range": "stddev: 0.005866860812937119",
            "extra": "mean: 3.007282784847293 msec\nrounds: 330"
          },
          {
            "name": "tests/bench.py::test_parse_binary_deep",
            "value": 252.77433834590374,
            "unit": "iter/sec",
            "range": "stddev: 0.00011968375288348899",
            "extra": "mean: 3.956097784861258 msec\nrounds: 251"
          }
        ]
      }
    ]
  }
}