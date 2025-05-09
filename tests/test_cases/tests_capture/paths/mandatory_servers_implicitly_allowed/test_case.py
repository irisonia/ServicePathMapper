from pathlib import Path

import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.common.strings.stats as output_stats
import tests.tests_strings as tests_common
from ...run_test_case import run_test_case


def test_mandatory_servers() -> None:
    run_test_case(_get_config(), _expected_results)


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 5,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a',
        program_args.ARG_MANDATORY_SERVERS: current_dir / 'mandatory_servers',
        program_args.ARG_ALLOWED_SERVERS: current_dir / 'allowed_servers'
    }


_expected_config_stats = {
    output_stats.OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "10",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 2,
            output_stats.OUTPUT_STATS_CLIENTS: ["a", "f"]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "8",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 1,
            output_stats.OUTPUT_STATS_CLIENTS: ["f"]
        },
    ],
    output_stats.OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "2",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 2,
            output_stats.OUTPUT_STATS_PROVIDERS: ["a", "b"]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "30",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 1,
            output_stats.OUTPUT_STATS_PROVIDERS: ["a"]
        }
    ],
    output_stats.OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT: [
        {output_stats.OUTPUT_STATS_SERVER: "f", output_stats.OUTPUT_STATS_SERVICES: ["12"]}
    ]
}

_expected_participation_in_paths_ctrs = {
    output_stats.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVERS: ['hello'],
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
            output_stats.OUTPUT_STATS_SERVER: "f",
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_GROUPS: 1,
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1
        },
    ],
    output_stats.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVICES: ["3"],
    output_stats.OUTPUT_STATS_ACTUAL_SERVICE_PARTICIPATION_CTR: [
        {output_stats.OUTPUT_STATS_SERVICE: "1", output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1},
        {output_stats.OUTPUT_STATS_SERVICE: "5", output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: 1}
    ],
    output_stats.OUTPUT_STATS_ACTUAL_SERVER_PAIR_ADJACENCY_CTR: [
        {
            output_stats.OUTPUT_STATS_ADJACENT_SERVERS: "a,f",
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_ADJACENCY: 1
        },
        {
            output_stats.OUTPUT_STATS_ADJACENT_SERVERS: "b,f",
            output_stats.OUTPUT_STATS_PARTICIPATION_COUNTER_ADJACENCY: 1
        },
    ]
}

_expected_paths = [
    {},
    {},
    {},
    {
        ('a', 'b', 'f'): [[('b', []), ('f', ['5']), ('a', ['1'])]]
    },
    {},
    {},
]

_expected_results = {
    tests_common.TESTS_OUTPUT_CONFIG_STATS: _expected_config_stats,
    tests_common.TESTS_OUTPUT_PARTICIPATION_CTRS: _expected_participation_in_paths_ctrs,
    tests_common.TESTS_OUTPUT_PATHS: _expected_paths
}
