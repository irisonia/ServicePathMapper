from dataclasses import dataclass

from servicepathmapper.common.types.printable import Printable


@dataclass
class InsufficientResources(Printable):
    def __str__(self) -> str:
        return f'Insufficient resources: {self.title}{self._format_values()}{self._format_help_topics()}'
