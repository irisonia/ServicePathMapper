import os
import tempfile
from pathlib import Path

from servicepathmapper.io.input.process_args import _read_lines_from_file


def test_read_lines_from_file():
    content = 'may\n\nthe force \nBE\n With You   \n'
    expected = {'may', 'the force', 'BE', 'With You'}

    with tempfile.NamedTemporaryFile('w+', delete=False) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        result = _read_lines_from_file(Path(temp_file_path))
        assert result == expected
    finally:
        os.remove(temp_file_path)
