from pathlib import Path

import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.common.strings.stats as output_stats
import tests.tests_strings as tests_common
from ...run_test_case import run_test_case


def test_config_stats_sorting() -> None:
    run_test_case(_get_config(), _expected_results)


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 5,
        program_args.ARG_SRC_SERVER: "b",
        program_args.ARG_DST_SERVER: "a",
        program_args.ARG_CONFIG_STATS_ONLY: True
    }


_expected_config_stats = {
    output_stats.OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "400",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 5,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "b",
                    "c",
                    "d",
                    "j",
                    "m"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "6",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 5,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "a",
                    "b",
                    "j",
                    "k",
                    "m"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "1",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 3,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "a",
                    "b",
                    "c"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "11",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 3,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "a",
                    "b",
                    "c"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "a2",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 1,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "a"
                ]
        },
    ],
    output_stats.OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "987",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 4,
            output_stats.OUTPUT_STATS_PROVIDERS:
                [
                    "d",
                    "j",
                    "k",
                    "m"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "4",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 3,
            output_stats.OUTPUT_STATS_PROVIDERS:
                [
                    "d",
                    "k",
                    "m"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "41",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 3,
            output_stats.OUTPUT_STATS_PROVIDERS:
                [
                    "d",
                    "k",
                    "m"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "98",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 1,
            output_stats.OUTPUT_STATS_PROVIDERS:
                [
                    "d"
                ]
        },
    ],
    output_stats.OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT: [
        {output_stats.OUTPUT_STATS_SERVER: "d", output_stats.OUTPUT_STATS_SERVICES: ["d1", "d2", "d3"]},
        {output_stats.OUTPUT_STATS_SERVER: "a1", output_stats.OUTPUT_STATS_SERVICES: ["a10", "a11"]},
        {output_stats.OUTPUT_STATS_SERVER: "a10", output_stats.OUTPUT_STATS_SERVICES: ["a101", "a102"]},
        {output_stats.OUTPUT_STATS_SERVER: "a", output_stats.OUTPUT_STATS_SERVICES: ["a1"]},
        {output_stats.OUTPUT_STATS_SERVER: "b", output_stats.OUTPUT_STATS_SERVICES: ["b1"]}
    ]
}

_expected_results = {tests_common.TESTS_OUTPUT_CONFIG_STATS: _expected_config_stats}
