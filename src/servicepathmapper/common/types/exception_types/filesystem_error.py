from dataclasses import dataclass

from servicepathmapper.common.types.printable import Printable


@dataclass
class FileSystemError(Printable, Exception):
    def __str__(self) -> str:
        return self._format('File system error')
