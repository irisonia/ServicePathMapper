from pathlib import Path

import pytest

from servicepathmapper.common.strings import program_args
from servicepathmapper.common.types.exception_types.bad_value_error import BadValueError
from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


def test_exception_src_server_not_in_clients_dir() -> None:
    with pytest.raises(BadValueError) as exc_info:
        main(_get_config(), DummyOutputGenerator())

    src_server = Path(exc_info.value.values[program_args.ARG_SRC_SERVER])
    assert src_server.name == 'Z'
    assert program_args.ARG_SRC_SERVER in exc_info.value.help_topics
    assert program_args.ARG_CLIENTS_DIR in exc_info.value.help_topics


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_SRC_SERVER: "Z",
        program_args.ARG_DST_SERVER: 'a',
        program_args.ARG_MAX_PATH_LEN: 3
    }
