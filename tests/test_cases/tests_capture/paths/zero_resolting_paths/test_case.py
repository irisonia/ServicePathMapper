from pathlib import Path

import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.common.strings.stats as output_stats

import tests.tests_strings as tests_common
from ...run_test_case import run_test_case


def test_zero_resulting_paths() -> None:
    run_test_case(_get_config(), _expected_results)


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 3,
        program_args.ARG_SRC_SERVER: "b",
        program_args.ARG_DST_SERVER: "a",
        program_args.ARG_FORBIDDEN_SERVICES: current_dir / 'forbidden_services',
        program_args.ARG_FORBIDDEN_SERVERS: current_dir / 'forbidden_servers'
    }


_expected_config_stats = {
    output_stats.OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "8",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 2,
            output_stats.OUTPUT_STATS_CLIENTS: ["e", "f"]

        },
    ],
    output_stats.OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS: [],
    output_stats.OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT: [
        {output_stats.OUTPUT_STATS_SERVER: "d", output_stats.OUTPUT_STATS_SERVICES: ["7", "9"]},
        {output_stats.OUTPUT_STATS_SERVER: "e", output_stats.OUTPUT_STATS_SERVICES: ["11"]}
    ]
}

_expected_participation_in_paths_ctrs = {
    output_stats.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVERS: ["a", "b", "d", "e", "f", "g"],
    output_stats.OUTPUT_STATS_ACTUAL_SERVER_PARTICIPATION_CTR: [],
    output_stats.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVICES: ["10", "12", "2", "3", "30", "4", "5"],
    output_stats.OUTPUT_STATS_ACTUAL_SERVICE_PARTICIPATION_CTR: [],
    output_stats.OUTPUT_STATS_ACTUAL_SERVER_PAIR_ADJACENCY_CTR: []
}

_expected_paths = [
    {},
    {},
    {},
    {}
]

_expected_results = {
    tests_common.TESTS_OUTPUT_CONFIG_STATS: _expected_config_stats,
    tests_common.TESTS_OUTPUT_PARTICIPATION_CTRS: _expected_participation_in_paths_ctrs,
    tests_common.TESTS_OUTPUT_PATHS: _expected_paths
}
