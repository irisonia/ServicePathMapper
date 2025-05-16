from collections import defaultdict
from pathlib import Path
from unittest.mock import patch

import pytest

from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.io.output_generators.file_system import _output_paths


def test_output_paths_raises_filesystem_error_on_write_failure(tmp_path):
    output_params = OutputGenerationParams(
        out_dir_path=tmp_path,
        entities=_get_test_entities(),
        config_stats={},
        participation_counters=None,
        stats_only=False,
        paths_by_servers_group_by_len=_get_paths(),
        max_threads=1,
        server_groups_only=False,
    )

    with patch.object(Path, "write_text", side_effect=OSError("disk full")):
        with pytest.raises(FileSystemError) as exc_info:
            _output_paths(output_params)
        assert "disk full" in exc_info.value.values.values()


def _get_test_entities() -> Entities:
    entities = Entities()
    entities.server_name_to_id = {
        'b': 0,
        'g': 1,
        'a': 2
    }
    entities.server_id_to_name = ['b', 'g', 'a']

    entities.service_name_to_id = {
        '3': 0,
        '2': 1,
        '1': 2,
        '20': 3
    }
    entities.service_id_to_name = ['3', '2', '1', '20']

    entities.services_of_provider = {
        1: [2],
        2: [3, 1, 0],
    }
    entities.providers_of_service = {
        0: [2],
        1: [2],
        2: [1],
        3: [2]
    }

    entities.services_of_client = {
        1: [0, 1],
        0: [2],
    }

    entities.clients_of_service = {
        0: [1],
        1: [1],
        2: [0],
        3: []
    }

    entities.providers_of_client = {
        0: [1],
        1: [2],
    }

    return entities


def _get_paths():
    return [
        defaultdict(list, {
            frozenset({2, 0, 1}): [[(0, []), (1, [2]), (2, [1, 0])]]
        })
    ]
