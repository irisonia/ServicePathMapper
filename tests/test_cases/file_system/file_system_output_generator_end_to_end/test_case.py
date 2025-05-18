import json
from collections import defaultdict
from pathlib import Path

import servicepathmapper.common.strings.file_names as file_names
import servicepathmapper.common.strings.stats as output_stats
from servicepathmapper.common.types.config_stats import ConfigStats
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.participation_in_paths_counters import ParticipationInPathsCounters
from servicepathmapper.common.types.paths_type_hints import PathsByServersGroupByLen
from servicepathmapper.io.output_generators.file_system import FileSystemOutputGenerator


def test_file_system_output_generator_end_to_end(tmp_path: Path) -> None:
    output_dir = Path(tmp_path) / 'output'
    actual_result = _run_output_generator(output_dir)
    _check_result(output_dir, actual_result)


def _run_output_generator(output_dir_path: Path) -> int:
    generator = FileSystemOutputGenerator(output_dir_path)
    entities = _get_test_entities()
    config_stats = _get_test_config_stats()
    paths = _get_paths_by_length_by_servers_group()
    participation_counters = _get_test_participation_counters(entities, config_stats, paths)
    return generator.generate_output(
        entities=entities,
        out_dir_path=output_dir_path,
        config_stats=config_stats,
        participation_counters=participation_counters,
        paths_by_path_length_by_servers_group=paths,
        server_groups_only=False,
        stats_only=False,
        stats_in_dir=False,
        max_threads=1
    )


def _check_result(output_dir: Path, result: int) -> None:
    assert result == 0

    assert output_dir.exists()

    stats_file = output_dir / file_names.OUTPUT_STATS_FILE_NAME
    assert stats_file.exists()
    actual_stats = json.loads(stats_file.read_text())
    assert actual_stats == _expected_stats

    paths_dir = output_dir / (file_names.OUTPUT_FILE_NAME_PART_PATH_LEN + '_3')
    assert paths_dir.exists(), f"paths dir: {str(paths_dir)}"

    group_file = paths_dir / ('0_' + file_names.OUTPUT_FILE_NAME_PART_SERVERS_GROUP)
    assert group_file.exists()
    actual_group_members = group_file.read_text()
    assert actual_group_members == _expected_group_members

    path_file = paths_dir / '0'
    assert path_file.exists()
    actual_paths = path_file.read_text()
    assert actual_paths == _expected_paths


def _get_test_entities() -> Entities:
    entities = Entities()
    entities.server_name_to_id = {
        'b': 0,
        'g': 1,
        'a': 2
    }
    entities.server_id_to_name = ['b', 'g', 'a']

    entities.service_name_to_id = {
        '3': 0,
        '2': 1,
        '1': 2,
        '20': 3
    }
    entities.service_id_to_name = ['3', '2', '1', '20']

    entities.services_of_provider = {
        1: [2],
        2: [3, 1, 0],
    }
    entities.providers_of_service = {
        0: [2],
        1: [2],
        2: [1],
        3: [2]
    }

    entities.services_of_client = {
        1: [0, 1],
        0: [2],
    }

    entities.clients_of_service = {
        0: [1],
        1: [1],
        2: [0],
        3: []
    }

    entities.providers_of_client = {
        0: [1],
        1: [2],
    }

    return entities


def _get_test_config_stats() -> ConfigStats:
    config_stats = ConfigStats()
    config_stats._services_with_providers_no_clients = {3: [2]}
    return config_stats


def _get_paths_by_length_by_servers_group() -> PathsByServersGroupByLen:
    return [
        defaultdict(list),
        defaultdict(list),
        defaultdict(list),
        defaultdict(list, {
            (2, 0, 1): [[(0, []), (1, [2]), (2, [1, 0])]]
        })
    ]


def _get_test_participation_counters(
        entities: Entities,
        config_stats: ConfigStats,
        paths_by_length_by_servers_group: PathsByServersGroupByLen) -> ParticipationInPathsCounters:
    return ParticipationInPathsCounters(entities, config_stats, paths_by_length_by_servers_group)


_expected_stats = {
    output_stats.OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS: [],
    output_stats.OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "20",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 1,
            output_stats.OUTPUT_STATS_PROVIDERS: ["a"]
        }
    ],
    output_stats.OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT: [],
    output_stats.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVERS: [],
    output_stats.OUTPUT_STATS_ACTUAL_SERVER_PARTICIPATION_CTR: [
        {
            output_stats.OUTPUT_STATS_SERVER: "a",
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_GROUPS: 1,
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1
        },
        {
            output_stats.OUTPUT_STATS_SERVER: "b",
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_GROUPS: 1,
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1
        },
        {
            output_stats.OUTPUT_STATS_SERVER: "g",
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_GROUPS: 1,
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1
        }
    ],
    output_stats.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVICES: [],
    output_stats.OUTPUT_STATS_ACTUAL_SERVICE_PARTICIPATION_CTR: [
        {output_stats.OUTPUT_STATS_SERVICE: "1", output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1},
        {output_stats.OUTPUT_STATS_SERVICE: "2", output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1},
        {output_stats.OUTPUT_STATS_SERVICE: "3", output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1}
    ],
    output_stats.OUTPUT_STATS_ACTUAL_SERVER_PAIR_ADJACENCY_CTR: [
        {
            output_stats.OUTPUT_STATS_ADJACENT_SERVERS: "a,g",
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_ADJACENCY: 1
        },
        {
            output_stats.OUTPUT_STATS_ADJACENT_SERVERS: "b,g",
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_ADJACENCY: 1
        },
    ]
}

_expected_group_members = 'a\nb\ng'

_expected_paths = 'b [1] g [2, 3] a'
