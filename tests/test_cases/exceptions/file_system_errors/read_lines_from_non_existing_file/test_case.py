from pathlib import Path
from unittest import mock

import pytest

from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.io.input.process_args import _read_lines_from_file


def test_read_lines_from_file_os_error():
    path = Path('some_file')
    with mock.patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with pytest.raises(FileSystemError) as exc_info:
            _read_lines_from_file(path)

        assert str(path) in str(exc_info.value.values) or str(path) in str(exc_info.value)
