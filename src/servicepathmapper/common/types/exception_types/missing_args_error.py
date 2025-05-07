from dataclasses import dataclass


@dataclass
class MissingArgsError(Exception):
    missing: list[str]

    def __str__(self) -> str:
        msg = f'Missing required args Error:\n{", ".join(self.missing)}'
        msg += f'\nRun with option --help to see which arguments are mandatory.'
        return msg
