from dataclasses import dataclass

from servicepathmapper.common.types.printable import Printable


@dataclass
class ConflictingArgsError(Printable, Exception):
    def __str__(self) -> str:
        return self._format('Conflicting args error')
