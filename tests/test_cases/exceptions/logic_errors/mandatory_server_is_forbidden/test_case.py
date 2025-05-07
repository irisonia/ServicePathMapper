from pathlib import Path

import pytest
import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.types.exception_types.logic_error import LogicError
from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


def test_exception_mandatory_server_is_forbidden() -> None:
    with pytest.raises(LogicError) as exc_info:
        main(_get_config(), DummyOutputGenerator())

    assert exc_info.value.values == {'server': ['c', 'f']}


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 5,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a',
        program_args.ARG_MANDATORY_SERVERS: current_dir / 'mandatory_servers',
        program_args.ARG_FORBIDDEN_SERVERS: current_dir / 'forbidden_servers'
    }
