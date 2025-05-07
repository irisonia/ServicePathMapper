import re
from pathlib import Path

VERSION = '0.1.0'

with open('pyproject.toml', 'r+') as f:
    content = f.read()
    content = re.sub(r'version\s*=\s*".*"', f'version = "{VERSION}"', content)
    f.seek(0)
    f.write(content)
    f.truncate()

Path('version.py').write_text(f"__version__ = '{VERSION}'\n")
