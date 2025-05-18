import re
from pathlib import Path

VERSION = '0.1.0'

script_dir = Path(__file__).parent
pyproject_path = script_dir.parent / 'pyproject.toml'
version_py_path = script_dir.parent / 'src' / 'servicepathmapper' / 'version.py'

# Update pyproject.toml
content = pyproject_path.read_text(encoding='utf-8')
# Only replace the first occurrence at line start
content_new = re.sub(
    r'(?m)^version\s*=\s*".*"$',
    f'version = "{VERSION}"',
    content
)
pyproject_path.write_text(content_new, encoding='utf-8')

# Update version.py
version_py_path.write_text(f"__version__ = '{VERSION}'\n", encoding='utf-8')
