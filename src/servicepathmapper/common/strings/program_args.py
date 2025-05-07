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
    '\n  cli: --clients-dir [path/to/clients/directory]'
    '\n  config: "clients-dir": "path/to/clients/directory"'
)

ARG_PROVIDERS_DIR_HELP_STR = (
    '(required) path to directory containing provider files'
    '\na provider file is named after a server and lists, one per line, all the services provided by this server'
    '\nexamples:'
    '\n  cli: --providers-dir [path/to/providers/directory]'
    '\n  config: "providers-dir": "path/to/providers/directory"'
)

ARG_SRC_SERVER_HELP_STR = (
    "(required) paths' start point server"
    '\nexamples:'
    '\n  cli: --src-server [src_server]'
    '\n  config: "src-server": "src_server"'
)

ARG_DST_SERVER_HELP_STR = (
    "(required) paths' end point server"
    '\nexamples:'
    '\n  cli: --dst-server [dst_server]'
    '\n  config: "dst-server": "dst_server"'
)

ARG_MIN_PATH_LEN_HELP_STR = (
    'minimum length of any path'
    f'\nmust be {constants.ARG_DEFAULT_MIN_PATH_LEN} or greater, and not greater than max-path-len'
    f'\nif not specified, default is {constants.ARG_DEFAULT_MIN_PATH_LEN}'
    '\nexamples:'
    '\n  cli: --min-path-len 2'
    '\n  config: "min-path-len": 2'
)

ARG_MAX_PATH_LEN_HELP_STR = (
    '(required) maximum length of any path'
    f'\nlimited to {constants.PATH_LEN_MAX_LIMIT} (can be carefully changed, if necessary)'
    '\nexamples:'
    '\n  cli: --max-path-len 4'
    '\n  config: "max-path-len": 4'
)

ARG_MANDATORY_SERVERS_HELP_STR = (
    'path to file that lists, one per line, names of servers that must participate in every path'
    '\nexamples:'
    '\n  cli: --mandatory-servers [path/to/mandatory/servers/file]'
    '\n  config: "mandatory-servers": "path/to/mandatory/servers/file"'
    '\nnotes:'
    '\n- src-server and dst-server servers are implicitly mandatory'
)

ARG_ALLOWED_SERVERS_HELP_STR = (
    'path to file that lists, one per line, names of servers allowed to participate in paths'
    '\nif not specified, all servers are allowed by default'
    '\nexamples:'
    '\n  cli: --allowed-servers [path/to/allowed/servers/file]'
    '\n  config: "allowed-servers": "path/to/allowed/servers/file"'
    '\nnotes:'
    '\n- mandatory servers are implicitly allowed'
    '\n- either supply allowed-servers or forbidden-servers, but not both'
)

ARG_FORBIDDEN_SERVERS_HELP_STR = (
    'path to file that lists, one per line, names of servers forbidden from participating in paths'
    '\nexamples:'
    '\n  cli: --forbidden-servers [path/to/forbidden/servers/file]'
    '\n  config: "forbidden-servers": "path/to/forbidden/servers/file"'
    '\nnotes:'
    '\n- either supply allowed-servers or forbidden-servers, but not both'
)

ARG_MANDATORY_SERVICES_HELP_STR = (
    'path to file that lists, one per line, names of services that must participate in every path'
    '\nexamples:'
    '\n  cli: --mandatory-services [path/to/mandatory/services/file]'
    '\n  config: "mandatory-services": "path/to/mandatory/services/file"'
)

ARG_ALLOWED_SERVICES_HELP_STR = (
    'path to file that lists, one per line, names of services allowed to participate in paths'
    '\nif not specified, all services are allowed by default'
    '\nexamples:'
    '\n  cli: --allowed-services [path/to/allowed/services/file]'
    '\n  config: "allowed-services": "path/to/allowed/services/file"'
    '\nnotes:'
    '\n- mandatory services are implicitly allowed'
    '\n- either supply allowed-services or forbidden-services, but not both'
)

ARG_FORBIDDEN_SERVICES_HELP_STR = (
    'path to file that lists, one per line, names of services forbidden from participating in paths'
    '\nexamples:'
    '\n  cli: --forbidden-services [path/to/forbidden/services/file]'
    '\n  config: "forbidden-services": "path/to/forbidden/services/file"'
    '\nnotes:'
    '\n- either supply allowed-services or forbidden-services, but not both'
)

ARG_STATS_ONLY_HELP_STR = (
    f'output {file_names.OUTPUT_STATS_FILE_NAME} file only, including config stats and participation counters'
    '\ndo not output paths files or server group files'
    '\nexamples:'
    '\n  cli: --stats-only, --no-stats-only'
    '\n  config: "stats-only": true, "stats-only": false'
)

ARG_CONFIG_STATS_ONLY_HELP_STR = (
    f'output {file_names.OUTPUT_STATS_FILE_NAME} file only, including only config stats'
    '\ndo not output paths files, server group files or participation counters'
    '\nwith this flag, paths are not calculated at all, useful for just analyzing a distributed system'
    '\nexamples:'
    '\n  cli: --config-stats-only, --no-config-stats-only'
    '\n  config: "config-stats-only": true, "config-stats-only": false'
)

ARG_SERVER_GROUPS_ONLY_HELP_STR = (
    f'output _{file_names.OUTPUT_FILE_NAME_PART_SERVERS_GROUP} files only, do not output paths files'
    f'\n{file_names.OUTPUT_STATS_FILE_NAME} is unaffected by this flag'
    '\nexamples:'
    '\n  cli: --server-groups-only, --no-server-groups-only'
    '\n  config: "server-groups-only": true, "server-groups-only": false'
)

ARG_MAX_THREADS_HELP_STR = (
    'maximum number of threads the program may use (default is based on cpu count)'
    '\nexamples:'
    '\n  cli: --max-threads 20'
    '\n  config: "max-threads": 20'
)

ARG_OUTPUT_DIR_HELP_STR = (
    'output directory path; by default, output is placed in a directory named after the run timestamp'
    f'\nwhich is placed under a common root directory: ./{file_names.OUTPUT_DEFAULT_ROOT_DIR_NAME}'
    '\nexamples:'
    '\n  cli: --output-dir [path/to/output/directory]'
    '\n  config: "output-dir": "path/to/output/directory"'
)

ARG_FORCE_LARGE_COMPUTATION_HELP_STR = (
    'override safety checks predicting very large computations and output sizes; use at your own risk'
    '\nexamples:'
    '\n  cli: --force-large-computation, --no-force-large-computation'
    '\n  config: "force-large-computation": true, "force-large-computation": false'
)
