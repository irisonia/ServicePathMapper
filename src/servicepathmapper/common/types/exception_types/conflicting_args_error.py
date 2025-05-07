from dataclasses import dataclass

from servicepathmapper.common.types.runtime_message_base import RuntimeMessageBase


@dataclass
class ConflictingArgsError(RuntimeMessageBase, Exception):
    def __str__(self) -> str:
        return self._format('Conflicting args error')
