from pathlib import Path

import servicepathmapper.common.constants as constants
import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.io.input.arg_info as arg_info
from servicepathmapper.common.types.exception_types.bad_value_error import BadValueError
from servicepathmapper.common.types.exception_types.conflicting_args_error import ConflictingArgsError
from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.common.types.exception_types.logic_error import LogicError
from servicepathmapper.common.types.exception_types.missing_args_error import MissingArgsError


def validate_args(args: dict) -> None:
    """
    Validate validity of args, combined from command line and from config file.

    Args:
        args (dict): Combined arguments from command-line, config file, and hard coded.

    Raises:
        BadValueError: For an invalid value (example: negative max-path-length).
        ConflictingArgsError: For conflicting arguments (example: allowed-servers + forbidden-servers).
        FileSystemError: For a file system related problem.
        LogicError: For logical inconsistency (example: a server that is both mandatory and forbidden).
        MissingArgsError: For a missing required argument.
    """

    _validate_required_args(args)
    _validate_servers_dirs(args)
    _validate_src_and_dst_servers(args)
    _validate_path_length(args)
    _validate_conflicting_args(args)


def _validate_required_args(args: dict) -> None:
    missing_required_args = [
        key for key, value in arg_info.ARG_INFO.items()
        if arg_info.ArgMetadata.REQUIRED & value.get(arg_info.ARG_METADATA, 0)
           and (key not in args or args[key] is None)
    ]
    if missing_required_args:
        raise MissingArgsError(missing=missing_required_args)


def _validate_servers_dirs(args: dict) -> None:
    clients_dir: Path = args[program_args.ARG_CLIENTS_DIR]
    providers_dir: Path = args[program_args.ARG_PROVIDERS_DIR]

    if not clients_dir.is_dir():
        raise FileSystemError(
            title=f'directory {clients_dir} not found',
            values={program_args.ARG_CLIENTS_DIR: clients_dir},
            help_topics=[program_args.ARG_CLIENTS_DIR]
        )
    if not providers_dir.is_dir():
        raise FileSystemError(
            title=f'directory {providers_dir} not found',
            values={program_args.ARG_PROVIDERS_DIR: providers_dir},
            help_topics=[program_args.ARG_PROVIDERS_DIR]
        )


def _validate_src_and_dst_servers(args: dict) -> None:
    clients_dir = Path(args[program_args.ARG_CLIENTS_DIR])
    providers_dir = Path(args[program_args.ARG_PROVIDERS_DIR])
    src_server: Path = args[program_args.ARG_SRC_SERVER]
    dst_server: Path = args[program_args.ARG_DST_SERVER]

    if src_server == dst_server:
        raise LogicError(
            title=f'{program_args.ARG_SRC_SERVER} and {program_args.ARG_DST_SERVER} are the same server',
            values={program_args.ARG_SRC_SERVER: src_server, program_args.ARG_DST_SERVER: dst_server},
            help_topics=[program_args.ARG_SRC_SERVER, program_args.ARG_DST_SERVER]
        )

    def is_file(dir_name, dir_arg, server_name, server_arg):
        if not (dir_name / server_name).is_file():
            raise BadValueError(
                title=f'file {server_arg} not found in {args[dir_arg]}',
                values={
                    server_arg: args[server_arg],
                    dir_arg: args[dir_arg]
                },
                help_topics=[server_arg, dir_arg]
            )
    is_file(clients_dir, program_args.ARG_CLIENTS_DIR, src_server, program_args.ARG_SRC_SERVER)
    is_file(providers_dir, program_args.ARG_PROVIDERS_DIR, dst_server, program_args.ARG_DST_SERVER)


def _validate_path_length(args: dict) -> None:
    if args[program_args.ARG_MAX_PATH_LEN] > constants.PATH_LEN_MAX_LIMIT:
        raise BadValueError(
            title=f'{program_args.ARG_MAX_PATH_LEN} too big. Limit max is {constants.PATH_LEN_MAX_LIMIT}',
            values={program_args.ARG_MAX_PATH_LEN: args[program_args.ARG_MAX_PATH_LEN]},
            help_topics=[program_args.ARG_MAX_PATH_LEN]
        )

    def _validate_min_value(arg_name: str, value: int, min_value: int) -> None:
        if value < min_value:
            raise BadValueError(
                title=f'{arg_name} must not be smaller than {min_value}',
                values={arg_name: value},
                help_topics=[arg_name]
            )
    _validate_min_value(arg_name=program_args.ARG_MIN_PATH_LEN,
                        value=args[program_args.ARG_MIN_PATH_LEN],
                        min_value=constants.ARG_DEFAULT_MIN_PATH_LEN)
    _validate_min_value(arg_name=program_args.ARG_MAX_PATH_LEN,
                        value=args[program_args.ARG_MAX_PATH_LEN],
                        min_value=constants.ARG_DEFAULT_MIN_PATH_LEN)

    if args[program_args.ARG_MIN_PATH_LEN] > args[program_args.ARG_MAX_PATH_LEN]:
        raise BadValueError(
            title=f'{program_args.ARG_MIN_PATH_LEN} is bigger than {program_args.ARG_MAX_PATH_LEN}',
            values={
                program_args.ARG_MIN_PATH_LEN: args[program_args.ARG_MIN_PATH_LEN],
                program_args.ARG_MAX_PATH_LEN: args[program_args.ARG_MAX_PATH_LEN]
            },
            help_topics=[program_args.ARG_MIN_PATH_LEN, program_args.ARG_MAX_PATH_LEN]
        )


def _validate_conflicting_args(args: dict) -> None:
    conflicting_pairs = [
        (program_args.ARG_ALLOWED_SERVERS, program_args.ARG_FORBIDDEN_SERVERS),
        (program_args.ARG_ALLOWED_SERVICES, program_args.ARG_FORBIDDEN_SERVICES)
    ]

    for arg1, arg2 in conflicting_pairs:
        if args.get(arg1) and args.get(arg2):
            raise ConflictingArgsError(
                title=f'Both {arg1} and {arg2} supplied',
                values={arg1: args[arg1], arg2: args[arg2]},
                help_topics=[arg1, arg2]
            )
