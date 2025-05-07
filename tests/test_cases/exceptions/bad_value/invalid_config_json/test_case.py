import tempfile
from pathlib import Path

import pytest
import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.types.exception_types.bad_value_error import BadValueError
from servicepathmapper.io.input.get_args import _load_config_file


def test_load_config_file_with_invalid_json():
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write("{ invalid json ]")
        tmp_path = Path(tmp.name)

    with pytest.raises(BadValueError) as exc_info:
        _load_config_file(str(tmp_path))

    err = exc_info.value
    assert "config" in err.values
    assert str(tmp_path) in err.values["config"]
    assert exc_info.value.help_topics == [program_args.ARG_HELP_CONFIG]

    tmp_path.unlink(missing_ok=True)
