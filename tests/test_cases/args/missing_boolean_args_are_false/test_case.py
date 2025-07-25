from pathlib import Path

import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.io.input import arg_info
from servicepathmapper.io.input.get_args import get_program_args


def test_missing_boolean_args_are_false():
    config = _get_config()
    config, _ = get_program_args(config)

    for args_key, args_info in arg_info.ARG_INFO.items():
        metadata = args_info.get(arg_info.ARG_METADATA, 0)
        if arg_info.ArgMetadata.BOOLEAN & metadata:
            assert config[args_key] is False


def _get_config() -> dict:
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 3,
        program_args.ARG_MIN_PATH_LEN: 2,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a'
    }
