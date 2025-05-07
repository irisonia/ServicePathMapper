from pathlib import Path


def config_to_jsonable(config: dict) -> dict:
    """Convert all Path values in config dict to str for JSON dumping."""

    return {k: str(v) if isinstance(v, Path) else v for k, v in config.items()}
