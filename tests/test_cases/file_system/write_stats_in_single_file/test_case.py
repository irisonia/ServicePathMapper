import json

import servicepathmapper.common.strings.file_names as file_names
import servicepathmapper.common.strings.stats as output_stats
from servicepathmapper.io.output_generators.file_system import _write_stats


_minimal_stats = {
    output_stats.OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS: [],
    output_stats.OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS: [
        {"service": "7000", "providers_count": 1, "providers": ["k"]}
    ],
    output_stats.OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT: [],
    output_stats.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVERS: [],
    output_stats.OUTPUT_STATS_ACTUAL_SERVER_PARTICIPATION_CTR: [],
    output_stats.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVICES: [],
    output_stats.OUTPUT_STATS_ACTUAL_SERVICE_PARTICIPATION_CTR: [],
    output_stats.OUTPUT_STATS_ADJACENT_SERVERS: [],
}


def test_write_stats_single_file(tmp_path):
    stats = _minimal_stats.copy()
    _write_stats(tmp_path, stats, stats_in_dir=False)
    stats_file = tmp_path / file_names.OUTPUT_STATS_FILE_NAME
    assert stats_file.exists() and stats_file.is_file()

    with stats_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    for key in _minimal_stats:
        assert key in data
        assert data[key] == _minimal_stats[key]
