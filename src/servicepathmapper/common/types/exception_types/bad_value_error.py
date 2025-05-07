from dataclasses import dataclass

from servicepathmapper.common.types.printable import Printable


@dataclass
class BadValueError(Printable, Exception):
    def __str__(self) -> str:
        return self._format('Bad value error')
