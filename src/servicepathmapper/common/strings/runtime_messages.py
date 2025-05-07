from dataclasses import dataclass

from servicepathmapper.common.types.runtime_message_base import RuntimeMessageBase


@dataclass
class InsufficientResources(RuntimeMessageBase):
    def __str__(self) -> str:
        return f'Insufficient resources: {self.title}{self._format_values()}{self._format_help_topics()}'
