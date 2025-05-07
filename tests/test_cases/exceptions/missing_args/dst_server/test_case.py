from pathlib import Path

import pytest
import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.types.exception_types.missing_args_error import MissingArgsError
from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


def test_exception_missing_program_arg_dst_server_and_max_path_len() -> None:
    with pytest.raises(MissingArgsError) as exc_info:
        main(_get_config(), DummyOutputGenerator())

    assert program_args.ARG_DST_SERVER in exc_info.value.missing
    assert program_args.ARG_MAX_PATH_LEN in exc_info.value.missing


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_SRC_SERVER: 'b'
    }
