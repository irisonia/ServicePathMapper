from dataclasses import dataclass

from servicepathmapper.common.types.runtime_message_base import RuntimeMessageBase


@dataclass
class FileSystemError(RuntimeMessageBase, Exception):
    def __str__(self) -> str:
        return self._format('File system error')
