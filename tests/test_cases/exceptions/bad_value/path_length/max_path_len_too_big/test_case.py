from pathlib import Path

import pytest
import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.constants import PATH_LEN_MAX_LIMIT
from servicepathmapper.common.types.exception_types.bad_value_error import BadValueError
from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


def test_exception_max_path_len_too_big() -> None:
    with pytest.raises(BadValueError) as exc_info:
        main(_get_config(), DummyOutputGenerator())

    assert exc_info.value.values == {program_args.ARG_MAX_PATH_LEN: PATH_LEN_MAX_LIMIT + 1}
    assert exc_info.value.help_topics == [program_args.ARG_MAX_PATH_LEN]


def _get_config() -> dict:
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: PATH_LEN_MAX_LIMIT + 1,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a'
    }
