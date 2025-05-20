import pytest

from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.exception_types.code_behavior_error import CodeBehaviorError
from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.io.output_generators.file_system import FileSystemOutputGenerator


class DummyEntities(Entities):
    pass


def test_generate_output_raises_code_behavior_error(tmp_path, mocker):
    output_dir = tmp_path / "output_subdir"

    params = OutputGenerationParams(
        entities=DummyEntities(),
        out_dir_path=output_dir,
        config_stats={},
        participation_counters={},
        paths_by_servers_group_by_len=None,
        server_groups_only=False,
        stats_only=False,
        stats_in_dir=False,
        max_threads=1
    )

    mocker.patch(
        "servicepathmapper.io.output_generators.file_system._output_stats",
        return_value=None
    )

    with pytest.raises(CodeBehaviorError, match="Paths is unexpectedly None!"):
        FileSystemOutputGenerator(output_dir)._generate_output(params)
