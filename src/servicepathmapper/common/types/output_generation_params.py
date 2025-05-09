from pathlib import Path

from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.paths_type_hints import PathsByServersGroupByLen


class OutputGenerationParams:
    """
    The data required for generating output.
    """

    def __init__(self,
                 entities: Entities,
                 out_dir_path: Path,
                 config_stats: dict,
                 participation_counters: dict | None,
                 paths_by_servers_group_by_len: PathsByServersGroupByLen | None,
                 stats_only: bool,
                 server_groups_only: bool,
                 max_threads: int):
        self.entities = entities
        self.out_dir_path = out_dir_path
        self.config_stats = config_stats
        self.participation_counters = participation_counters
        self.paths_by_servers_group_by_len = paths_by_servers_group_by_len
        self.stats_only = stats_only
        self.server_groups_only = server_groups_only
        self.max_threads = max_threads
