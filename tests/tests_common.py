from pathlib import Path

from servicepathmapper.common.strings import program_args


def config_to_jsonable(config: dict) -> dict:
    """Convert all Path values in config dict to str for JSON dumping."""

    return {k: str(v) if isinstance(v, Path) else v for k, v in config.items()}


def default_config_args(output_dir_path: Path) -> dict:
    return {
        program_args.ARG_OUTPUT_DIR: output_dir_path,
        program_args.ARG_SERVER_GROUPS_ONLY: False,
        program_args.ARG_STATS_ONLY: False,
        program_args.ARG_OUTPUT_STATS_IN_DIR: False,
        program_args.ARG_MAX_THREADS: 1
    }
