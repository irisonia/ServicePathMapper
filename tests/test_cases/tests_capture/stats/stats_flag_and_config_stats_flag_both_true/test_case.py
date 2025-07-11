from pathlib import Path

import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.common.strings.stats as output_stats
import tests.tests_strings as tests_common
from ...run_test_case import run_test_case


def test_stats_flag_and_config_stats_flag_both_true() -> None:
    run_test_case(_get_config(), _expected_results)


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 5,
        program_args.ARG_SRC_SERVER: "b",
        program_args.ARG_DST_SERVER: "a",
        program_args.ARG_STATS_ONLY: True,
        program_args.ARG_CONFIG_STATS_ONLY: True
    }


_expected_config_stats = {
    output_stats.OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "8",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 3,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "c",
                    "e",
                    "f"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "8000",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 1,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "x"
                ]
        },
    ],
    output_stats.OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "7000",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 1,
            output_stats.OUTPUT_STATS_PROVIDERS:
                [
                    "y"
                ]
        },
    ],
    output_stats.OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT: [
        {output_stats.OUTPUT_STATS_SERVER: "d", output_stats.OUTPUT_STATS_SERVICES: ["7", "9"]},
        {output_stats.OUTPUT_STATS_SERVER: "e", output_stats.OUTPUT_STATS_SERVICES: ["11"]}
    ]
}

_expected_results = {tests_common.TESTS_OUTPUT_CONFIG_STATS: _expected_config_stats}
