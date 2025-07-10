import pytest

from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.exception_types.code_behavior_error import CodeBehaviorError
from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.io.output_generators.file_system import FileSystemOutputGenerator
from tests.tests_common import default_config_args


class DummyEntities(Entities):
    pass


def test_generate_output_raises_code_behavior_error(tmp_path, mocker):
    output_dir = tmp_path / "output_subdir"

    params = OutputGenerationParams(
        entities=DummyEntities(),
        config_stats={},
        config_args=default_config_args(output_dir),
        participation_counters={},
        paths_by_servers_group_by_len=None
    )

    mocker.patch(
        "servicepathmapper.io.output_generators.file_system._output_stats",
        return_value=None
    )

    with pytest.raises(CodeBehaviorError, match="Paths is unexpectedly None!"):
        FileSystemOutputGenerator(output_dir)._generate_output(params)
