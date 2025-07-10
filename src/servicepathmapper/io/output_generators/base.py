from abc import abstractmethod, ABC

from servicepathmapper.common.types.config_stats import ConfigStats
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.common.types.participation_in_paths_counters import ParticipationInPathsCounters
from servicepathmapper.common.types.paths_type_hints import PathsByServersGroupByLen


class OutputGenerator(ABC):
    def generate_output(
            self,
            entities: Entities,
            config_stats: ConfigStats,
            config_args: dict,
            participation_counters: ParticipationInPathsCounters | None,
            paths_by_path_length_by_servers_group: PathsByServersGroupByLen | None) -> int | dict:
        """
        Generates output for the program, either for a regular run or for tests.

        Returns:
            Either success status int, for a regular run, or the actual results, for tests.

        Raises:
            NotImplementedError exception, in case of derived class missing an implementation.
        """

        params = OutputGenerationParams(
            entities=entities,
            config_stats=config_stats.get(entities),
            config_args=config_args,
            participation_counters=None if participation_counters is None else participation_counters.get(),
            paths_by_servers_group_by_len=paths_by_path_length_by_servers_group)
        return self._generate_output(params)

    @abstractmethod
    def _generate_output(self, params: OutputGenerationParams) -> int | dict:
        raise NotImplementedError
