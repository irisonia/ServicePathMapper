from pathlib import Path

import pytest

import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.types.exception_types.bad_type_error import BadTypeError
from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


def test_int_arg_bad_type(monkeypatch):
    with pytest.raises(BadTypeError) as exc_info:
        main(_get_config(), DummyOutputGenerator())

    assert exc_info.value.values == {program_args.ARG_MAX_PATH_LEN: 'not-an-int'}
    assert exc_info.value.help_topics == [program_args.ARG_MAX_PATH_LEN]


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 'not-an-int',
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a'
    }
