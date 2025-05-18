"""
Acceptable program arguments and their attributes.
"""

from enum import IntFlag, auto

import servicepathmapper.common.strings.program_args as program_args

ARG_HELP: str = 'help'
ARG_METADATA: str = 'metadata'


class ArgMetadata(IntFlag):
    BOOLEAN = auto()
    HELP = auto()
    REQUIRED = auto()
    INT = auto()
    PATH = auto()


ARG_INFO = {
    program_args.ARG_HELP_CONFIG: {
        ARG_HELP: program_args.ARG_HELP_CONFIG_HELP_STR,
        ARG_METADATA: ArgMetadata.HELP,
    },
    program_args.ARG_HELP_OUTPUT: {
        ARG_HELP: program_args.ARG_HELP_OUTPUT_HELP_STR,
        ARG_METADATA: ArgMetadata.HELP,
    },
    program_args.ARG_HELP_STATS: {
        ARG_HELP: program_args.ARG_HELP_STATS_HELP_STR,
        ARG_METADATA: ArgMetadata.HELP,
    },
    program_args.ARG_HELP_PATHS: {
        ARG_HELP: program_args.ARG_HELP_PATHS_HELP_STR,
        ARG_METADATA: ArgMetadata.HELP,
    },
    program_args.ARG_CLIENTS_DIR: {
        ARG_HELP: program_args.ARG_CLIENTS_DIR_HELP_STR,
        ARG_METADATA: ArgMetadata.REQUIRED | ArgMetadata.PATH,
    },
    program_args.ARG_PROVIDERS_DIR: {
        ARG_HELP: program_args.ARG_PROVIDERS_DIR_HELP_STR,
        ARG_METADATA: ArgMetadata.REQUIRED | ArgMetadata.PATH,
    },
    program_args.ARG_SRC_SERVER: {
        ARG_HELP: program_args.ARG_SRC_SERVER_HELP_STR,
        ARG_METADATA: ArgMetadata.REQUIRED | ArgMetadata.PATH,
    },
    program_args.ARG_DST_SERVER: {
        ARG_HELP: program_args.ARG_DST_SERVER_HELP_STR,
        ARG_METADATA: ArgMetadata.REQUIRED | ArgMetadata.PATH,
    },
    program_args.ARG_MIN_PATH_LEN: {
        ARG_HELP: program_args.ARG_MIN_PATH_LEN_HELP_STR,
        ARG_METADATA: ArgMetadata.INT,
    },
    program_args.ARG_MAX_PATH_LEN: {
        ARG_HELP: program_args.ARG_MAX_PATH_LEN_HELP_STR,
        ARG_METADATA: ArgMetadata.REQUIRED | ArgMetadata.INT,
    },
    program_args.ARG_MANDATORY_SERVERS: {
        ARG_HELP: program_args.ARG_MANDATORY_SERVERS_HELP_STR,
        ARG_METADATA: ArgMetadata.PATH,
    },
    program_args.ARG_ALLOWED_SERVERS: {
        ARG_HELP: program_args.ARG_ALLOWED_SERVERS_HELP_STR,
        ARG_METADATA: ArgMetadata.PATH,
    },
    program_args.ARG_FORBIDDEN_SERVERS: {
        ARG_HELP: program_args.ARG_FORBIDDEN_SERVERS_HELP_STR,
        ARG_METADATA: ArgMetadata.PATH,
    },
    program_args.ARG_MANDATORY_SERVICES: {
        ARG_HELP: program_args.ARG_MANDATORY_SERVICES_HELP_STR,
        ARG_METADATA: ArgMetadata.PATH,
    },
    program_args.ARG_ALLOWED_SERVICES: {
        ARG_HELP: program_args.ARG_ALLOWED_SERVICES_HELP_STR,
        ARG_METADATA: ArgMetadata.PATH,
    },
    program_args.ARG_FORBIDDEN_SERVICES: {
        ARG_HELP: program_args.ARG_FORBIDDEN_SERVICES_HELP_STR,
        ARG_METADATA: ArgMetadata.PATH,
    },
    program_args.ARG_STATS_ONLY: {
        ARG_HELP: program_args.ARG_STATS_ONLY_HELP_STR,
        ARG_METADATA: ArgMetadata.BOOLEAN,
    },
    program_args.ARG_CONFIG_STATS_ONLY: {
        ARG_HELP: program_args.ARG_CONFIG_STATS_ONLY_HELP_STR,
        ARG_METADATA: ArgMetadata.BOOLEAN,
    },
    program_args.ARG_OUTPUT_STATS_IN_DIR: {
        ARG_HELP: program_args.ARG_OUTPUT_STATS_IN_DIR_HELP_STR,
        ARG_METADATA: ArgMetadata.BOOLEAN,
    },
    program_args.ARG_SERVER_GROUPS_ONLY: {
        ARG_HELP: program_args.ARG_SERVER_GROUPS_ONLY_HELP_STR,
        ARG_METADATA: ArgMetadata.BOOLEAN,
    },
    program_args.ARG_MAX_THREADS: {
        ARG_HELP: program_args.ARG_MAX_THREADS_HELP_STR,
        ARG_METADATA: ArgMetadata.INT,
    },
    program_args.ARG_OUTPUT_DIR: {
        ARG_HELP: program_args.ARG_OUTPUT_DIR_HELP_STR,
        ARG_METADATA: ArgMetadata.PATH,
    },
    program_args.ARG_FORCE_LARGE_COMPUTATION: {
        ARG_HELP: program_args.ARG_FORCE_LARGE_COMPUTATION_HELP_STR,
        ARG_METADATA: ArgMetadata.BOOLEAN,
    }
}
