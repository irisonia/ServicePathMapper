import json

import servicepathmapper.common.strings.stats as output_stats
from servicepathmapper.common.strings import file_names
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


def test_write_stats_in_dir(tmp_path):
    stats = _minimal_stats.copy()
    _write_stats(tmp_path, stats, stats_in_dir=True)

    stats_dir = tmp_path / file_names.OUTPUT_STATS_DIR_NAME
    assert stats_dir.exists() and stats_dir.is_dir()

    for key, value in _minimal_stats.items():
        stat_file = stats_dir / key
        assert stat_file.exists() and stat_file.is_file()
        if value:
            with stat_file.open("r", encoding="utf-8") as f:
                content = json.load(f)
            assert list(content.keys()) == [key]
            assert content[key] == value
        else:
            assert stat_file.read_text(encoding="utf-8") == ""
