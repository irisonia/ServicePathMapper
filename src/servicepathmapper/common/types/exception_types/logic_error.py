from dataclasses import dataclass

from servicepathmapper.common.types.printable import Printable


@dataclass
class LogicError(Printable, Exception):
    def __str__(self) -> str:
        return self._format('Logic error')
