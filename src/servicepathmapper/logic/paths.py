import logging
from collections import defaultdict

import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.common.types.paths_type_hints as paths_types
from servicepathmapper.common.logger import Logger
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.runtime_messages import EarlyDetectNoPaths


def map_paths(entities: Entities,
              src_server_name: str,
              dst_server_name: str,
              min_path_len: int,
              max_path_len: int) -> paths_types.PathsByServersGroupByLen:
    return _Paths(entities=entities,
                  src_server_name=src_server_name,
                  dst_server_name=dst_server_name,
                  min_path_len=min_path_len,
                  max_path_len=max_path_len).map_paths()


class _Paths:
    def __init__(self,
                 entities: Entities,
                 src_server_name: str,
                 dst_server_name: str,
                 min_path_len: int,
                 max_path_len: int):
        self._src_server_name = src_server_name
        self._dst_server_name = dst_server_name
        self._min_path_len = min_path_len
        self._max_path_len = max_path_len
        self._entities = entities

        self._paths_by_size: paths_types.PathsByServersGroupByLen = [
            defaultdict(list) for _ in range(max_path_len + 1)
        ]
        self._dst_server_id = self._entities.server_name_to_id[self._dst_server_name]  # frequently used
        self._visited = set()
        # memorize dead-end states by path's last server and visited servers
        self._server_dead_end_visited_state = defaultdict(set)

    def map_paths(self) -> paths_types.PathsByServersGroupByLen:
        if not self._validate_potential_for_paths():
            return []
        src_server_id = self._entities.server_name_to_id[self._src_server_name]
        self._visited.add(src_server_id)
        self._dfs([(src_server_id, [])])
        return self._paths_by_size

    def _validate_potential_for_paths(self) -> bool:
        condition_1 = self._validate_enough_servers_for_min_path_len()
        condition_2 = self._validate_mandatory_servers_may_participate()
        condition_3 = self._validate_mandatory_services_may_participate()
        return condition_1 and condition_2 and condition_3

    def _validate_enough_servers_for_min_path_len(self) -> bool:
        """Early detect not having enough servers to create a path of the required minimal length."""

        total_servers = len(self._entities.server_name_to_id)
        if total_servers < self._min_path_len:
            Logger.log(str(
                EarlyDetectNoPaths(
                    title=f'Not enough servers for {program_args.ARG_MIN_PATH_LEN}.',
                    values={'servers': total_servers, program_args.ARG_MIN_PATH_LEN: self._min_path_len},
                    help_topics=[program_args.ARG_MIN_PATH_LEN])),
                level=logging.INFO)
            return False
        return True

    def _validate_mandatory_services_may_participate(self) -> bool:
        """Early detect a required service unable to participate in paths."""

        services = [s for s in self._entities.mandatory_services_names if s not in self._entities.service_name_to_id]
        if services:
            Logger.log(str(
                EarlyDetectNoPaths(
                    title="Mandatory services cannot participate.",
                    values={'services': ', '.join(f'"{s}"' for s in services)},
                    help_topics=[program_args.ARG_MANDATORY_SERVICES])),
                level=logging.INFO)
            return False
        return True

    def _validate_mandatory_servers_may_participate(self) -> bool:
        """Early detect a required server unable to participate in paths."""

        servers = [s for s in self._entities.mandatory_servers_names if s not in self._entities.server_name_to_id]
        if servers:
            Logger.log(str(
                EarlyDetectNoPaths(
                    title="Mandatory servers cannot participate.",
                    values={'servers': ', '.join(f'"{s}"' for s in servers)},
                    help_topics=[program_args.ARG_MANDATORY_SERVERS])),
                level=logging.INFO)
            return False
        return True

    def _dfs(self, path: paths_types.ServiceBasedPath) -> bool:
        dfs_continuity_check_result = self._dfs_continue_check(path)
        if dfs_continuity_check_result is not None:  # stop recursing: completed path or no chance for a path
            if dfs_continuity_check_result:
                self._on_path(path)
            return dfs_continuity_check_result

        current_last_server_in_path = path[-1][0]
        any_path_found = False
        for candidate_to_join_path in self._entities.providers_of_client[current_last_server_in_path]:
            if not candidate_to_join_path in self._visited:
                service_ids = list(self._entities.services_of_client[current_last_server_in_path]
                                   & self._entities.services_of_provider[candidate_to_join_path])
                path.append((candidate_to_join_path, service_ids))
                self._visited.add(candidate_to_join_path)
                any_path_found |= self._dfs(path)
                self._visited.remove(candidate_to_join_path)
                path.pop()
        if not any_path_found:
            self._server_dead_end_visited_state[current_last_server_in_path].add(frozenset(self._visited))
        return any_path_found

    def _dfs_continue_check(self, path: paths_types.ServiceBasedPath) -> bool | None:
        current_last_server_in_path = path[-1][0]
        if current_last_server_in_path == self._dst_server_id:
            return self._is_path_valid(path)
        if len(path) == self._max_path_len:
            return False
        if (current_last_server_in_path in self._server_dead_end_visited_state) and \
                (frozenset(self._visited) in self._server_dead_end_visited_state[current_last_server_in_path]):
            return False
        return None

    def _is_path_valid(self, path: paths_types.ServiceBasedPath) -> bool:
        if len(path) < self._min_path_len:
            return False
        if not self._validate_mandatory(path):
            return False
        return True

    def _validate_mandatory(self, path: paths_types.ServiceBasedPath) -> bool:
        mandatory_servers_ids = set(self._entities.server_name_to_id[name]
                                    for name in self._entities.mandatory_servers_names)
        mandatory_services_ids = set(self._entities.service_name_to_id[name]
                                     for name in self._entities.mandatory_services_names)

        servers_in_path = set(server_id for server_id, _ in path)
        services_in_path = set(service_id for _, services_ids in path for service_id in services_ids)

        return (mandatory_servers_ids.issubset(servers_in_path)
                and mandatory_services_ids.issubset(services_in_path))

    def _on_path(self, path: paths_types.ServiceBasedPath) -> None:
        groups_of_size = self._paths_by_size[len(path)]
        key = frozenset(server_id for server_id, _ in path)
        groups_of_size[key].append(path.copy())
