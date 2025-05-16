from pathlib import Path

import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.io.input.get_args import get_program_args
from servicepathmapper.io.input.process_args import process_program_args


def test_src_and_dst_servers_automatically_mandatory():
    config = _get_config()
    args, _ = get_program_args(config)
    entities, _ = process_program_args(args=args)

    assert entities.mandatory_servers_names == {'a', 'b'}


def _get_config() -> dict:
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 3,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a'
    }
