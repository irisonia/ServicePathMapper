from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Printable(ABC):
    title: str
    values: Optional[dict[str, Any]] = field(default_factory=dict)
    help_topics: Optional[list[str]] = field(default_factory=list)

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def _format(self, title: str) -> str:
        return f'{title}:\n{self.title}{self._format_values()}{self._format_help_topics()}'

    def _format_values(self) -> str:
        return '\n' + '\n'.join(f'{k}: {v}' for k, v in self.values.items()) if self.values else ''

    def _format_help_topics(self) -> str:
        if self.help_topics:
            topics_str = ', '.join(f'--{topic}' for topic in self.help_topics)
            return f'\nRun with option --help, and see {topics_str}'
        return ''
