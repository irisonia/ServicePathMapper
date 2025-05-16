from dataclasses import dataclass

from servicepathmapper.common.types.printable import Printable


@dataclass
class EarlyDetectNoPaths(Printable):
    common_title = 'No paths can be generated'

    def __str__(self) -> str:
        s = f'\n{self.common_title}: {self.title}{self._format_values()}{self._format_help_topics()}'
        return s
