import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import servicepathmapper.common.constants as constants
import servicepathmapper.common.strings.about as program_info
import servicepathmapper.common.strings.file_names as file_names
import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.io.input.arg_info as arg_info
from servicepathmapper.common.types.exception_types.bad_type_error import BadTypeError
from servicepathmapper.common.types.exception_types.bad_value_error import BadValueError
from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.io.input.validate_args import validate_args
from servicepathmapper.version import __version__


def get_program_args(test_config: dict | None = None) -> tuple[dict, set]:
    """
    Collect and validate program arguments from command line, a configuration file, and hardcoded.

    Args:
        test_config: Preknown config dict, used by tests only.

    Returns:
        A tuple containing:
            - A dict: A dictionary containing the program's configuration options.
            - A set: A set containing help related options.

    Raises:
        BadTypeError: For an argument type that is not as expected.
        BadValueError: For an invalid value (example: negative max-path-length).
        ConflictingArgsError: For conflicting arguments (example: allowed-servers + forbidden-servers).
        FileSystemError: For a file system related problem.
        LogicError: For logical inconsistency (example: a server that is both mandatory and forbidden).
        MissingArgsError: For a missing required argument.
    """

    raw_args = _get_args_from_user() if test_config is None else test_config
    args, help_args = _categorize_args(raw_args)

    if len(help_args) == 0:
        _normalize_args_types(args)
        _normalize_args_values(args)
        validate_args(args)

    return args, help_args


def _get_args_from_user() -> dict:
    """
    Get arguments provided in command line and in config, with higher precedence to command line.
    :return: A dict containing all arguments.
    :raises FileSystemError: If the config file cannot be read.
    :raises BadValueError: If the config file is not valid JSON.
    """

    cli_args = _make_parser().parse_args()
    final_args = {}

    if cli_args.config:
        config_data = _load_config_file(cli_args.config)
        final_args.update(config_data)

    for arg, value in vars(cli_args).items():
        if arg == 'config':
            continue
        if value is not None:
            final_args[arg] = value

    return final_args


def _load_config_file(config_path: str | Path) -> dict:
    """
    Load and return the config JSON from the given path.

    :param config_path: Path to the config file.
    :return: Parsed config data as a dictionary.
    :raises FileSystemError: If the file cannot be opened.
    :raises BadValueError: If the file content is not valid JSON.
    """

    config_path = Path(config_path)

    try:
        content = config_path.read_text(encoding='utf-8')
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise BadValueError(
                title=f'Invalid JSON in config file: {config_path}',
                values={'config': str(config_path), 'error': str(e)},
                help_topics=[program_args.ARG_HELP_CONFIG]
            )
    except OSError as e:
        raise FileSystemError(
            title=f'Failed to read config file: {config_path}',
            values={'config': str(config_path), 'error': str(e)},
            help_topics=[program_args.ARG_HELP_CONFIG]
        )


def _make_parser() -> argparse.ArgumentParser:
    """
    Create an argparse parser to read command line arguments.
    :return: The built parser object.
    """

    parser = argparse.ArgumentParser(
        prog='python3 -m ' + program_info.PACKAGE_NAME + '.' + program_info.MODULE_NAME,
        description=program_info.PACKAGE_DESCRIPTION,
        epilog=f'For more details, visit {program_info.GIT_PATH}',
        formatter_class=argparse.RawTextHelpFormatter,
        conflict_handler='resolve',
        add_help=False)

    args_group_general, args_group_help, args_group_config = _create_parser_groups(parser)
    _add_args_to_parser_groups(args_group_help, args_group_config)

    return parser


def _create_parser_groups(parser: argparse.ArgumentParser) -> tuple[Any, Any, Any]:
    args_group_general = parser.add_argument_group('general options')
    args_group_general.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args_group_general.add_argument('--config', dest='config', help='config file path', metavar='[path]')

    args_group_help = parser.add_argument_group('help options')
    args_group_help.add_argument('-h', '--help', action='help', help='show this help message and exit')

    args_group_config = parser.add_argument_group('configuration options')

    return args_group_general, args_group_help, args_group_config


def _add_args_to_parser_groups(args_group_help: Any, args_group_config: Any) -> None:
    for args_key, args_info in arg_info.ARG_INFO.items():
        metadata = args_info.get(arg_info.ARG_METADATA, 0)
        if arg_info.ArgMetadata.HELP & metadata:
            args_group_help.add_argument(
                f'--{args_key}',
                dest=args_key,
                help=args_info[program_args.ARG_HELP],
                action='store_true',
                default=None
            )
        elif arg_info.ArgMetadata.BOOLEAN & metadata:
            help_str = args_info[program_args.ARG_HELP]
            args_group_config.add_argument(
                f'--{args_key}',
                dest=args_key,
                action='store_true',
                default=None,
                help=help_str
            )
            args_group_config.add_argument(
                f'--no-{args_key}',
                dest=args_key,
                action='store_false',
                default=None,
                help=f'Use this to set `{args_key}` to false on the command line'
            )
        else:
            args_group_config.add_argument(
                f'--{args_key}',
                dest=args_key,
                help=args_info[program_args.ARG_HELP]
            )


def _categorize_args(args: dict) -> tuple[dict, set[str]]:
    """
    Categorizes args into config args and help args.
    :param args: Combined arguments from command-line, config file, and hard coded.
    """

    config_args = dict()
    help_args = set()

    for arg_name, arg_value in args.items():
        if arg_name not in arg_info.ARG_INFO:
            continue
        arg_metadata = arg_info.ARG_INFO[arg_name].get(arg_info.ARG_METADATA, 0)
        if arg_metadata & arg_info.ArgMetadata.HELP:
            help_args.add(arg_name)
        else:
            config_args[arg_name] = arg_value

    return config_args, help_args


def _normalize_args_types(args: dict) -> None:
    """
    Normalize argument types in-place (bool, int, Path).
    :param args: Combined arguments from command-line, config file, and hard coded.
    :raises BadTypeError: for an argument type that is not as expected.
    """

    for key, info in arg_info.ARG_INFO.items():
        if key in args:
            args[key] = _normalize_arg_by_type(key, info, args[key])


def _normalize_arg_by_type(key: str, info: dict[str, Any], val: Any) -> Any:
    metadata = info.get(arg_info.ARG_METADATA, 0)
    if metadata & arg_info.ArgMetadata.BOOLEAN:
        return _normalize_arg_boolean(key, val)
    if metadata & arg_info.ArgMetadata.INT:
        return _normalize_arg_int(key, val)
    if metadata & arg_info.ArgMetadata.PATH:
        return _normalize_arg_path(key, val)
    return val


def _normalize_arg_boolean(key: str, val: Any) -> bool:
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        val_lower = val.lower()
        if val_lower in ('true', '1'):
            return True
        if val_lower in ('false', '0'):
            return False
        raise BadTypeError(
            title=f"Invalid boolean value for '{key}'",
            values={key: val},
            help_topics=[key]
        )
    if isinstance(val, int):
        if (val == 1) or (val == 0):
            return bool(val)
        raise BadTypeError(
            title=f"Invalid integer boolean value for '{key}'",
            values={key: val},
            help_topics=[key]
        )
    raise BadTypeError(
        title=f"Invalid boolean value type for '{key}'",
        values={key: val},
        help_topics=[key]
    )


def _normalize_arg_int(key: str, val: Any) -> int | None:
    if val is not None and not isinstance(val, int):
        try:
            return int(val)
        except (ValueError, TypeError):
            raise BadTypeError(
                title=f"Invalid integer value for '{key}'",
                values={key: val},
                help_topics=[key]
            )
    return val


def _normalize_arg_path(key: str, val: str | Path) -> Path | None:
    illegal_paths = ['', '.', '..']
    if (val is None) or (str(val).strip() in illegal_paths):
        raise BadValueError(
            title=f'Illegal value for arg {key}',
            values={key: val},
            help_topics=[key]
        )
    if not isinstance(val, Path):
        return Path(val)
    return val


def _normalize_args_values(args: dict) -> None:
    """
    Set defaults when needed, and recognize args implied by other args.
    :param args: Combined arguments from command-line, config file, and hard coded.
    """

    for key, info in arg_info.ARG_INFO.items():
        metadata = info.get(arg_info.ARG_METADATA, 0)
        if metadata & arg_info.ArgMetadata.BOOLEAN and key not in args:
            args[key] = False

    if program_args.ARG_MIN_PATH_LEN not in args:
        args[program_args.ARG_MIN_PATH_LEN] = constants.ARG_DEFAULT_MIN_PATH_LEN

    if args.get(program_args.ARG_CONFIG_STATS_ONLY) is True:
        args[program_args.ARG_STATS_ONLY] = True

    if program_args.ARG_MAX_THREADS not in args:
        args[program_args.ARG_MAX_THREADS] = constants.ARG_DEFAULT_MAX_THREADS

    if program_args.ARG_OUTPUT_DIR not in args:
        timestamp = datetime.now().strftime(file_names.OUTPUT_DIR_NAME_TEMPLATE)
        args[program_args.ARG_OUTPUT_DIR] = Path(file_names.OUTPUT_DEFAULT_ROOT_DIR_NAME) / timestamp
