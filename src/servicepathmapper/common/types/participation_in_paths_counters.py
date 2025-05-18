from collections import defaultdict

import servicepathmapper.common.strings.stats as stats_strings
from servicepathmapper.common.types.config_stats import ConfigStats
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.paths_type_hints import PathsByServersGroupByLen


class ParticipationInPathsCounters:
    """
    Numerical summaries about the participation of servers and of services in the resulting paths.
    """

    def __init__(self,
                 entities: Entities,
                 config_stats: ConfigStats,
                 paths_by_servers_group_by_len: PathsByServersGroupByLen):
        self._config_stats = config_stats
        self._entities = entities
        self._server_participation_ctr = defaultdict(int)
        self._service_participation_ctr = defaultdict(int)
        self._servers_adjacency_ctr = defaultdict(int)
        self._num_groups_of_server = defaultdict(int)

        self._count(paths_by_servers_group_by_len)

    def get(self) -> dict:
        services_out_of_scope = (
                set(self._config_stats._services_with_providers_no_clients)
                | {item for value in
                   self._config_stats._services_unreachable_for_sole_provider_client.values()
                   for item
                   in value})

        return {
            stats_strings.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVERS: sorted(
                [
                    value for key, value
                    in enumerate(self._entities.server_id_to_name)
                    if (key not in self._num_groups_of_server)
                ],
            ),
            stats_strings.OUTPUT_STATS_ACTUAL_SERVER_PARTICIPATION_CTR: sorted(
                [
                    {
                        stats_strings.OUTPUT_STATS_SERVER: self._entities.server_id_to_name[item[0]],
                        stats_strings.OUTPUT_STATS_PARTICIPATION_COUNTER_GROUPS: self._num_groups_of_server[item[0]],
                        stats_strings.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: item[1]
                    }
                    for item in self._server_participation_ctr.items() if item[1] > 0
                ],
                key=lambda item: (-item[stats_strings.OUTPUT_STATS_PARTICIPATION_COUNTER_GROUPS],
                                  -item[stats_strings.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS],
                                  item[stats_strings.OUTPUT_STATS_SERVER]),
            ),
            stats_strings.OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVICES: sorted(
                [
                    value for key, value in enumerate(self._entities.service_id_to_name) if
                    key not in self._service_participation_ctr
                    and key not in services_out_of_scope
                ],
            ),
            stats_strings.OUTPUT_STATS_ACTUAL_SERVICE_PARTICIPATION_CTR: sorted(
                [
                    {stats_strings.OUTPUT_STATS_SERVICE: self._entities.service_id_to_name[item[0]],
                     stats_strings.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS: item[1]}
                    for item in self._service_participation_ctr.items() if item[1] > 0
                ],
                key=lambda item: (
                    -item[stats_strings.OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS],
                    item[stats_strings.OUTPUT_STATS_SERVICE]),
            ),
            stats_strings.OUTPUT_STATS_ACTUAL_SERVER_PAIR_ADJACENCY_CTR: sorted(
                [
                    {
                        stats_strings.OUTPUT_STATS_ADJACENT_SERVERS: ','.join(
                            sorted([self._entities.server_id_to_name[item[0][0]],
                                    self._entities.server_id_to_name[item[0][1]]])),
                        stats_strings.OUTPUT_STATS_PARTICIPATION_COUNTER_ADJACENCY: item[1]
                    }
                    for item in self._servers_adjacency_ctr.items()
                ],
                key=lambda item: (
                    -item[stats_strings.OUTPUT_STATS_PARTICIPATION_COUNTER_ADJACENCY],
                    item[stats_strings.OUTPUT_STATS_ADJACENT_SERVERS]),
            )
        }

    def _count(self, paths_by_servers_group_by_len: PathsByServersGroupByLen) -> None:
        for length in paths_by_servers_group_by_len:
            for group, paths_of_group in length.items():
                for server in group:
                    self._num_groups_of_server[server] += 1
                for path in paths_of_group:
                    for server, services in path:
                        self._server_participation_ctr[server] += 1
                        for service in services:
                            self._service_participation_ctr[service] += 1

                    for i in range(1, len(path)):
                        server1 = path[i - 1][0]
                        server2 = path[i][0]
                        key = tuple(sorted((server1, server2)))
                        self._servers_adjacency_ctr[key] += 1
