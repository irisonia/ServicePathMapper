from pathlib import Path

import pytest

import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.types.exception_types.bad_value_error import BadValueError
from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


@pytest.mark.parametrize("bad_value", ['', '.', '..', '    .   ', '   ..   '])
def test_exception_illegal_clients_dir(bad_value):
    config = _get_config()
    config[program_args.ARG_CLIENTS_DIR] = bad_value
    with pytest.raises(BadValueError) as exc_info:
        main(config, DummyOutputGenerator())
    assert str(exc_info.value.values[program_args.ARG_CLIENTS_DIR]).strip() == bad_value.strip()
    assert program_args.ARG_CLIENTS_DIR in exc_info.value.help_topics


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 5,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a'
    }
