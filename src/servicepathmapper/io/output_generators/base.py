from abc import abstractmethod, ABC
from pathlib import Path

from servicepathmapper.common.types.config_stats import ConfigStats
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.common.types.participation_in_paths_counters import ParticipationInPathsCounters
from servicepathmapper.common.types.paths_type_hints import PathsByServersGroupByLen


class OutputGenerator(ABC):
    def generate_output(
            self,
            entities: Entities,
            out_dir_path: Path,
            config_stats: ConfigStats,
            participation_counters: ParticipationInPathsCounters | None,
            paths_by_path_length_by_servers_group: PathsByServersGroupByLen | None,
            server_groups_only: bool,
            stats_only: bool,
            max_threads: int) -> int | dict:
        """
        Generates output for the program, either for a regular run or for tests.

        Returns:
            Either success status int, for a regular run, or the actual results, for tests.

        Raises:
            NotImplementedError exception, in case of derived class missing an implementation.
        """

        config_stats_json = config_stats.to_json(entities)
        participation_counters_json = None if participation_counters is None else participation_counters.to_json()

        params = OutputGenerationParams(
            entities=entities,
            out_dir_path=out_dir_path,
            config_stats=config_stats_json,
            participation_counters=participation_counters_json,
            paths_by_servers_group_by_len=paths_by_path_length_by_servers_group,
            server_groups_only=server_groups_only,
            stats_only=stats_only,
            max_threads=max_threads)
        return self._generate_output(params)

    @abstractmethod
    def _generate_output(self, params: OutputGenerationParams) -> int | dict:
        raise NotImplementedError
