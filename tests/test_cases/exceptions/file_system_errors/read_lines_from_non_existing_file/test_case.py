from pathlib import Path

import pytest

from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.io.input.process_args import _read_lines_from_file


def test_read_lines_from_non_existing_file():
    non_existent_path = Path('non_existent_file')
    with pytest.raises(FileSystemError) as exc_info:
        _read_lines_from_file(non_existent_path)

    assert exc_info.value.values == {'path': str(non_existent_path)}
