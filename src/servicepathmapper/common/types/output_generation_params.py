from servicepathmapper.common.strings import program_args
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.paths_type_hints import PathsByServersGroupByLen


class OutputGenerationParams:
    """
    The data required for generating output.
    """

    def __init__(self,
                 entities: Entities,
                 config_stats: dict,
                 config_args: dict,
                 participation_counters: dict | None,
                 paths_by_servers_group_by_len: PathsByServersGroupByLen | None):
        self.entities = entities
        self.out_dir_path = config_args[program_args.ARG_OUTPUT_DIR]
        self.config_stats = config_stats
        self.participation_counters = participation_counters
        self.paths_by_servers_group_by_len = paths_by_servers_group_by_len
        self.stats_only = config_args[program_args.ARG_STATS_ONLY]
        self.stats_in_dir = config_args[program_args.ARG_OUTPUT_STATS_IN_DIR]
        self.server_groups_only = config_args[program_args.ARG_SERVER_GROUPS_ONLY]
        self.max_threads = config_args[program_args.ARG_MAX_THREADS]
