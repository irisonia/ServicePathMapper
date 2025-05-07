from unittest import mock

import pytest
import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.io.input.get_args import _load_config_file


def test_load_config_file_os_error():
    config_path = "non_existent_file.json"

    with mock.patch("builtins.open", mock.Mock(side_effect=OSError("File not found"))):
        with pytest.raises(FileSystemError) as exc_info:
            _load_config_file(config_path)

        assert config_path in exc_info.value.title
        assert config_path in exc_info.value.values.values()
        assert exc_info.value.help_topics == [program_args.ARG_HELP_CONFIG]
