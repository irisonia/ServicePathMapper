import re
from pathlib import Path


def update_version(pyproject_path: Path, version_py_path: Path, version: str):
    content = pyproject_path.read_text(encoding='utf-8')
    content_new = re.sub(
        r'(?m)^version\s*=\s*".*"$',
        f'version = "{version}"',
        content
    )
    pyproject_path.write_text(content_new, encoding='utf-8')
    version_py_path.write_text(f"__version__ = '{version}'\n", encoding='utf-8')


def test_update_version(tmp_path):
    # Setup dummy pyproject.toml and version.py
    pyproject = tmp_path / "pyproject.toml"
    version_py = tmp_path / "version.py"
    pyproject.write_text('name = "mypkg"\nversion = "0.0.1"\n')
    version_py.write_text("__version__ = '0.0.1'\n")

    # Run the update
    update_version(pyproject, version_py, "1.2.3")

    # Assert pyproject.toml updated
    pyproject_content = pyproject.read_text()
    assert 'version = "1.2.3"' in pyproject_content
    assert 'version = "0.0.1"' not in pyproject_content

    # Assert version.py updated
    version_content = version_py.read_text()
    assert version_content == "__version__ = '1.2.3'\n"
