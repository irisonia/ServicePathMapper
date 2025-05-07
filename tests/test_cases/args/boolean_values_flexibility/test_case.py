from pathlib import Path

import pytest
import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


@pytest.mark.parametrize("input_val,expected", [
    ("true", True),
    ("TRUE", True),
    ("1", True),
    (1, True),
    (True, True),
    ("false", False),
    ("FALSE", False),
    ("0", False),
    (0, False),
    (False, False),
    (None, False)
])
def test_boolean_value_flexibility(input_val, expected):
    main(_get_config(input_val), DummyOutputGenerator())


def _get_config(input_val):
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 2,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a',
        program_args.ARG_CONFIG_STATS_ONLY: input_val
    }
