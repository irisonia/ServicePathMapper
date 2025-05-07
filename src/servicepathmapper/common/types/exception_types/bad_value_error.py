from dataclasses import dataclass

from servicepathmapper.common.types.runtime_message_base import RuntimeMessageBase


@dataclass
class BadValueError(RuntimeMessageBase, Exception):
    def __str__(self) -> str:
        return self._format('Bad value error')
