from pathlib import Path

import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.constants import PATH_LEN_MAX_LIMIT
from servicepathmapper.common.types.runtime_messages import EarlyDetectNoPaths
from ..run_test_case_with_log_message import run_test_case_with_log_message


def test_log_insufficient_resources_for_goal(caplog) -> None:
    run_test_case_with_log_message(
        config=_get_config(),
        expected_values={'servers': '7', program_args.ARG_MIN_PATH_LEN: PATH_LEN_MAX_LIMIT},
        expected_help_topics=[program_args.ARG_MIN_PATH_LEN],
        expected_common_title=EarlyDetectNoPaths.common_title,
        caplog=caplog
    )


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MIN_PATH_LEN: 15,
        program_args.ARG_MAX_PATH_LEN: 15,
        program_args.ARG_SRC_SERVER: "b",
        program_args.ARG_DST_SERVER: "a"
    }
