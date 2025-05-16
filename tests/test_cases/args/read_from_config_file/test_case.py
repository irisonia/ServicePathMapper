import json
from pathlib import Path

import pytest

import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.io.input.get_args import get_program_args
from tests.tests_common import config_to_jsonable


@pytest.fixture
def tmp_config(tmp_path: Path) -> str:
    """Create a temporary config file."""

    config_data = _get_config()
    config_file_path = tmp_path / "test_config.json"
    with config_file_path.open('w') as config_file:
        json.dump(config_to_jsonable(config_data), config_file)
    return str(config_file_path)


def test_read_from_config_file(monkeypatch, tmp_config) -> None:
    monkeypatch.setattr('sys.argv', ['prog', '--config', tmp_config])
    args, _ = get_program_args()
    current_dir = Path(__file__).resolve().parent

    assert args[program_args.ARG_ALLOWED_SERVICES] == current_dir / 'allowed_services'
    assert args[program_args.ARG_CLIENTS_DIR] == current_dir / 'clients'
    assert args[program_args.ARG_CONFIG_STATS_ONLY] is True
    assert str(args[program_args.ARG_DST_SERVER]) == 'a'
    assert args[program_args.ARG_FORBIDDEN_SERVERS] == current_dir / 'forbidden_servers'
    assert args[program_args.ARG_FORCE_LARGE_COMPUTATION] is True
    assert args[program_args.ARG_MANDATORY_SERVERS] == current_dir / 'mandatory_servers'
    assert args[program_args.ARG_MANDATORY_SERVICES] == current_dir / 'mandatory_services'
    assert args[program_args.ARG_MAX_PATH_LEN] == 10
    assert args[program_args.ARG_MAX_THREADS] == 100
    assert args[program_args.ARG_MIN_PATH_LEN] == 6
    assert args[program_args.ARG_OUTPUT_DIR] == current_dir / 'out_dir'
    assert args[program_args.ARG_PROVIDERS_DIR] == current_dir / 'providers'
    assert args[program_args.ARG_SERVER_GROUPS_ONLY] is True
    assert str(args[program_args.ARG_SRC_SERVER]) == 'b'
    assert args[program_args.ARG_STATS_ONLY] is True


def _get_config() -> dict:
    current_dir = Path(__file__).resolve().parent

    return {
        program_args.ARG_ALLOWED_SERVICES: current_dir / 'allowed_services',
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_CONFIG_STATS_ONLY: True,
        program_args.ARG_DST_SERVER: 'a',
        program_args.ARG_FORBIDDEN_SERVERS: current_dir / 'forbidden_servers',
        program_args.ARG_FORCE_LARGE_COMPUTATION: True,
        program_args.ARG_MANDATORY_SERVERS: current_dir / 'mandatory_servers',
        program_args.ARG_MANDATORY_SERVICES: current_dir / 'mandatory_services',
        program_args.ARG_MAX_PATH_LEN: 10,
        program_args.ARG_MAX_THREADS: 100,
        program_args.ARG_MIN_PATH_LEN: 6,
        program_args.ARG_OUTPUT_DIR: current_dir / 'out_dir',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_SERVER_GROUPS_ONLY: True,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_STATS_ONLY: True
    }
