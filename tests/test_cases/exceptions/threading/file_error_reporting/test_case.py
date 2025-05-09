from unittest.mock import patch

import pytest

from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.io.output_generators.file_system import FileSystemOutputGenerator


class DummyEntities(Entities):
    pass


def _make_dummy_output_params(output_dir):
    class DummyParams:
        entities = DummyEntities()
        out_dir_path = output_dir
        config_stats = {}
        participation_counters = {}
        stats_only = False
        server_groups_only = False
        max_threads = 2
        # The group keys and order will result in files named "0" and "1"
        paths_by_servers_group_by_len = [
            {
                frozenset([1]): [["fail"]],
                frozenset([2]): [["ok"]],
            }
        ]

    return DummyParams()


def test_file_error_reporting(tmp_path):
    output_dir = tmp_path / "output"

    # Patch _output_group to raise for the file named "0"
    def fake_output_group(entities, file_path, group_and_paths, groups_only):
        # file_path will be output_dir / "0" or output_dir / "1"
        if file_path.name == "0":
            raise RuntimeError("Simulated failure for file 0")

    output_gen = FileSystemOutputGenerator(output_dir)
    with patch.object(output_gen, "_output_group", side_effect=fake_output_group):
        params = _make_dummy_output_params(output_dir)
        with pytest.raises(FileSystemError) as excinfo:
            output_gen._output_paths(params)
        # The error should mention the file name "0" and the simulated error message
        assert "0" in str(excinfo.value)
        assert "Simulated failure for file 0" in str(excinfo.value)
