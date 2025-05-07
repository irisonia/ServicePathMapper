from pathlib import Path

import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.common.strings.stats as output_stats

import tests.tests_strings as tests_common
from ...run_test_case import run_test_case


# - forbidden servers: e, x, y
#
# - e is a client of services 8 and 11. 11 is provided by no one, 8 is provided by the forbidden server y.
# 8 has another clients, that are not forbidden (c, f).
# therefore: 8 is to be included in the list of services with clients but no providers,
# with the clients: c, f
#
# - x is client of 1000, 2000, which are provided by no one.
# 1000 has another client, that is also forbidden (y).
# 2000 has another client, that is not forbidden (b).
# therefore: 2000 is to be included in the list of services with clients but no providers,
# with the client: b
#
# - y is a client of services 1000, 3000, 4000, 5000.
# 1000 has another client, that is also forbidden (x).
# 4000 has another client, that is not forbidden (g).
# 1000 is provided by no one.
# 3000 is provided by the forbidden server x only.
# 4000 is provided by the forbidden servers x and y, and by the non-forbidden server d.
# 5000 is provided by no one.
# therefore: none is to be included in the list of services with clients but no providers.


def test_config_stats_only_with_forbidden_servers() -> None:
    run_test_case(_get_config(), _expected_results)


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 5,
        program_args.ARG_SRC_SERVER: "b",
        program_args.ARG_DST_SERVER: "a",
        program_args.ARG_CONFIG_STATS_ONLY: True,
        program_args.ARG_FORBIDDEN_SERVERS: current_dir / 'forbidden_servers',
    }


_expected_config_stats = {
    output_stats.OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "8",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 2,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "c",
                    "f"
                ]
        },
        {
            output_stats.OUTPUT_STATS_SERVICE: "2000",
            output_stats.OUTPUT_STATS_CLIENTS_COUNTER: 1,
            output_stats.OUTPUT_STATS_CLIENTS:
                [
                    "b"
                ]
        },
    ],
    output_stats.OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS: [
        {
            output_stats.OUTPUT_STATS_SERVICE: "30",
            output_stats.OUTPUT_STATS_PROVIDERS_COUNTER: 1,
            output_stats.OUTPUT_STATS_PROVIDERS:
                [
                    "a"
                ]
        },
    ],
    output_stats.OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT: [
        {output_stats.OUTPUT_STATS_SERVER: "d", output_stats.OUTPUT_STATS_SERVICES: ["7", "9"]}
    ]
}

_expected_results = {tests_common.TESTS_OUTPUT_CONFIG_STATS: _expected_config_stats}
