import servicepathmapper.common.constants as constants
import servicepathmapper.common.strings.file_names as file_names

ARG_HELP = 'help'
ARG_HELP_VERSION = 'version'
ARG_HELP_CONFIG = 'help-config'
ARG_HELP_OUTPUT = 'help-output'
ARG_HELP_STATS = 'help-stats'
ARG_HELP_PATHS = 'help-paths'

ARG_CLIENTS_DIR = 'clients-dir'
ARG_PROVIDERS_DIR = 'providers-dir'
ARG_SRC_SERVER = 'src-server'
ARG_DST_SERVER = 'dst-server'
ARG_MIN_PATH_LEN = 'min-path-len'
ARG_MAX_PATH_LEN = 'max-path-len'
ARG_MANDATORY_SERVERS = 'mandatory-servers'
ARG_ALLOWED_SERVERS = 'allowed-servers'
ARG_FORBIDDEN_SERVERS = 'forbidden-servers'
ARG_MANDATORY_SERVICES = 'mandatory-services'
ARG_ALLOWED_SERVICES = 'allowed-services'
ARG_FORBIDDEN_SERVICES = 'forbidden-services'
ARG_STATS_ONLY = 'stats-only'
ARG_CONFIG_STATS_ONLY = 'config-stats-only'
ARG_SERVER_GROUPS_ONLY = 'server-groups-only'
ARG_MAX_THREADS = 'max-threads'
ARG_OUTPUT_DIR = 'output-dir'
ARG_FORCE_LARGE_COMPUTATION = 'force-large-computation'

ARG_HELP_CONFIG_HELP_STR = 'show help about the program\'s configuration file and exit'
ARG_HELP_OUTPUT_HELP_STR = 'show help about the program\'s output and exit'
ARG_HELP_STATS_HELP_STR = 'show help about the program\'s statistics output file and exit'
ARG_HELP_PATHS_HELP_STR = 'show help about the program\'s paths output files and exit'

ARG_CLIENTS_DIR_HELP_STR = (
    '(required) path to directory containing client files'
    '\na client file is named after a server and lists, one per line, all the services accessible to this server'
    '\nexamples:'
    f'\n  cli: --{ARG_CLIENTS_DIR} [path/to/clients/directory]'
    f'\n  config: "{ARG_CLIENTS_DIR}": "path/to/clients/directory"'
)

ARG_PROVIDERS_DIR_HELP_STR = (
    '(required) path to directory containing provider files'
    '\na provider file is named after a server and lists, one per line, all the services provided by this server'
    '\nexamples:'
    f'\n  cli: --{ARG_PROVIDERS_DIR} [path/to/providers/directory]'
    f'\n  config: "{ARG_PROVIDERS_DIR}": "path/to/providers/directory"'
)

ARG_SRC_SERVER_HELP_STR = (
    '(required) starting server for paths'
    '\nexamples:'
    f'\n  cli: --{ARG_SRC_SERVER} [src_server]'
    f'\n  config: "{ARG_SRC_SERVER}": "src_server"'
)

ARG_DST_SERVER_HELP_STR = (
    '(required) destination server for paths'
    '\nexamples:'
    f'\n  cli: --{ARG_DST_SERVER} [dst_server]'
    f'\n  config: "{ARG_DST_SERVER}": "dst_server"'
)

ARG_MIN_PATH_LEN_HELP_STR = (
    'minimum length of any path'
    f'\nmust be {constants.ARG_DEFAULT_MIN_PATH_LEN} or greater, and not greater than {ARG_MAX_PATH_LEN}'
    f'\nif not specified, default is {constants.ARG_DEFAULT_MIN_PATH_LEN}'
    '\nexamples:'
    f'\n  cli: --{ARG_MIN_PATH_LEN} 2'
    f'\n  config: "{ARG_MIN_PATH_LEN}": 2'
)

ARG_MAX_PATH_LEN_HELP_STR = (
    '(required) maximum length of any path'
    f'\nlimited to {constants.PATH_LEN_MAX_LIMIT} (can be changed with caution)'
    '\nexamples:'
    f'\n  cli: --{ARG_MAX_PATH_LEN} 4'
    f'\n  config: "{ARG_MAX_PATH_LEN}": 4'
)

ARG_MANDATORY_SERVERS_HELP_STR = (
    'path to file that lists, one per line, names of servers that must participate in every path'
    '\nexamples:'
    f'\n  cli: --{ARG_MANDATORY_SERVERS} [path/to/mandatory/servers/file]'
    f'\n  config: "{ARG_MANDATORY_SERVERS}": "path/to/mandatory/servers/file"'
    '\nnotes:'
    f'\n- {ARG_SRC_SERVER} and {ARG_DST_SERVER} servers are implicitly mandatory'
)

ARG_ALLOWED_SERVERS_HELP_STR = (
    'path to file that lists, one per line, names of servers allowed to participate in paths'
    '\nif not specified, all servers are allowed by default'
    '\nexamples:'
    f'\n  cli: --{ARG_ALLOWED_SERVERS} [path/to/allowed/servers/file]'
    f'\n  config: "{ARG_ALLOWED_SERVERS}": "path/to/allowed/servers/file"'
    '\nnotes:'
    '\n- mandatory servers are implicitly allowed'
    f'\n- either supply {ARG_ALLOWED_SERVERS} or {ARG_FORBIDDEN_SERVERS}, but not both'
)

ARG_FORBIDDEN_SERVERS_HELP_STR = (
    'path to file that lists, one per line, names of servers forbidden from participating in paths'
    '\nif not specified, no servers are forbidden by default'
    '\nexamples:'
    f'\n  cli: --{ARG_FORBIDDEN_SERVERS} [path/to/forbidden/servers/file]'
    f'\n  config: "{ARG_FORBIDDEN_SERVERS}": "path/to/forbidden/servers/file"'
    '\nnotes:'
    f'\n- either supply {ARG_ALLOWED_SERVERS} or {ARG_FORBIDDEN_SERVERS}, but not both'
)

ARG_MANDATORY_SERVICES_HELP_STR = (
    'path to file that lists, one per line, names of services that must participate in every path'
    '\nexamples:'
    f'\n  cli: --{ARG_MANDATORY_SERVICES} [path/to/mandatory/services/file]'
    f'\n  config: "{ARG_MANDATORY_SERVICES}": "path/to/mandatory/services/file"'
)

ARG_ALLOWED_SERVICES_HELP_STR = (
    'path to file that lists, one per line, names of services allowed to participate in paths'
    '\nif not specified, all services are allowed by default'
    '\nexamples:'
    f'\n  cli: --{ARG_ALLOWED_SERVICES} [path/to/allowed/services/file]'
    f'\n  config: "{ARG_ALLOWED_SERVICES}": "path/to/allowed/services/file"'
    '\nnotes:'
    '\n- mandatory services are implicitly allowed'
    f'\n- either supply {ARG_ALLOWED_SERVICES} or {ARG_FORBIDDEN_SERVICES}, but not both'
)

ARG_FORBIDDEN_SERVICES_HELP_STR = (
    'path to file that lists, one per line, names of services forbidden from participating in paths'
    '\nexamples:'
    f'\n  cli: --{ARG_FORBIDDEN_SERVICES} [path/to/forbidden/services/file]'
    f'\n  config: "{ARG_FORBIDDEN_SERVICES}": "path/to/forbidden/services/file"'
    '\nnotes:'
    f'\n- either supply {ARG_ALLOWED_SERVICES} or {ARG_FORBIDDEN_SERVICES}, but not both'
)

ARG_STATS_ONLY_HELP_STR = (
    'output config stats and participation counters only, do not output paths or server groups'
    '\nexamples:'
    f'\n  cli: --{ARG_STATS_ONLY}, --no-{ARG_STATS_ONLY}'
    f'\n  config: "{ARG_STATS_ONLY}": true, "{ARG_STATS_ONLY}": false'
)

ARG_CONFIG_STATS_ONLY_HELP_STR = (
    'output config stats only, do not output paths, server groups or participation counters'
    '\nif set, paths are not calculated at all, useful for just analyzing a distributed system'
    '\nexamples:'
    f'\n  cli: --{ARG_CONFIG_STATS_ONLY}, --no-{ARG_CONFIG_STATS_ONLY}'
    f'\n  config: "{ARG_CONFIG_STATS_ONLY}": true, "{ARG_CONFIG_STATS_ONLY}": false'
    '\nnotes:'
    f'\nif {ARG_CONFIG_STATS_ONLY}, then {ARG_STATS_ONLY} is implicitly true'
)

ARG_SERVER_GROUPS_ONLY_HELP_STR = (
    f'output _{file_names.OUTPUT_FILE_NAME_PART_SERVERS_GROUP} files only, do not output paths files'
    '\nstats output is unaffected by this flag'
    '\nexamples:'
    f'\n  cli: --{ARG_SERVER_GROUPS_ONLY}, --no-{ARG_SERVER_GROUPS_ONLY}'
    f'\n  config: "{ARG_SERVER_GROUPS_ONLY}": true, "{ARG_SERVER_GROUPS_ONLY}": false'
)

ARG_MAX_THREADS_HELP_STR = (
    'maximum number of threads the program may use (default is based on cpu count)'
    '\nexamples:'
    f'\n  cli: --{ARG_MAX_THREADS} 20'
    f'\n  config: "{ARG_MAX_THREADS}": 20'
)

ARG_OUTPUT_DIR_HELP_STR = (
    'output directory path; by default, output is placed in a directory named after the run timestamp'
    f'\nwhich is placed under a common root directory: "./{file_names.OUTPUT_DEFAULT_ROOT_DIR_NAME}"'
    '\nexamples:'
    f'\n  cli: --{ARG_OUTPUT_DIR} [path/to/output/directory]'
    f'\n  config: "{ARG_OUTPUT_DIR}": "path/to/output/directory"'
)

ARG_FORCE_LARGE_COMPUTATION_HELP_STR = (
    'override safety checks predicting very large computations and output sizes; use at your own risk'
    '\nexamples:'
    f'\n  cli: --{ARG_FORCE_LARGE_COMPUTATION}, --no-{ARG_FORCE_LARGE_COMPUTATION}'
    f'\n  config: "{ARG_FORCE_LARGE_COMPUTATION}": true, "{ARG_FORCE_LARGE_COMPUTATION}": false'
)
