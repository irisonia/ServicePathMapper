from dataclasses import dataclass


@dataclass
class CodeBehaviorError(Exception):
    error: str

    def __str__(self) -> str:
        return f'There seems to be an error:\n{self.error}'
