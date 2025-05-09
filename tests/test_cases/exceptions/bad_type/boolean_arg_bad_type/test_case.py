from pathlib import Path

import pytest

import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.types.exception_types.bad_type_error import BadTypeError
from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


@pytest.mark.parametrize("input_val", [
    "a",
    "",
    2,
    -1,
    42,
    0.5,
    [],
    {},
    object(),
    "yes",
    "No",
    "not_a_boolean"
])
def test_boolean_arg_bad_type(input_val) -> None:
    with pytest.raises(BadTypeError) as exc_info:
        main(_get_config(input_val), DummyOutputGenerator())

    assert exc_info.value.values == {program_args.ARG_STATS_ONLY: input_val}
    assert exc_info.value.help_topics == [program_args.ARG_STATS_ONLY]


def _get_config(input_val):
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 2,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a',
        program_args.ARG_STATS_ONLY: input_val
    }
