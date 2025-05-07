import pytest
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.exception_types.code_behavior_alert import CodeBehaviorAlert
from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.io.output_generators.file_system import FileSystemOutputGenerator


class DummyEntities(Entities):
    pass


def test_generate_output_raises_on_none_paths(tmp_path):
    output_dir = tmp_path / "output_subdir"
    output_gen = FileSystemOutputGenerator(output_dir)
    params = OutputGenerationParams(
        entities=DummyEntities(),
        out_dir_path=output_dir,
        config_stats={},
        participation_counters={},
        paths_by_servers_group_by_len=None,
        server_groups_only=False,
        stats_only=False,
        max_threads=1
    )
    with pytest.raises(CodeBehaviorAlert):
        output_gen._generate_output(params)
