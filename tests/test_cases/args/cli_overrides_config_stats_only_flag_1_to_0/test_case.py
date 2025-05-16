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
    with open(config_file_path, 'w') as config_file:
        json.dump(config_to_jsonable(config_data), config_file)
    return str(config_file_path)


def test_cli_overrides_config_stats_only_flag_1_to_0(monkeypatch, tmp_config) -> None:
    """Test CLI args override config file values"""

    monkeypatch.setattr('sys.argv', ['prog', '--config', tmp_config, '--no-stats-only'])

    args, _ = get_program_args()
    assert args[program_args.ARG_STATS_ONLY] == 0


def _get_config():
    current_dir = Path(__file__).resolve().parent
    return {
        program_args.ARG_CLIENTS_DIR: current_dir / 'clients',
        program_args.ARG_PROVIDERS_DIR: current_dir / 'providers',
        program_args.ARG_MAX_PATH_LEN: 3,
        program_args.ARG_STATS_ONLY: True,
        program_args.ARG_SRC_SERVER: 'b',
        program_args.ARG_DST_SERVER: 'a'
    }
