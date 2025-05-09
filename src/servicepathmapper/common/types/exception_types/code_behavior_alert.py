from dataclasses import dataclass


@dataclass
class CodeBehaviorAlert(Exception):
    alert: str

    def __str__(self) -> str:
        return f'Code behavior is suspicious:\n{self.alert}'
