import concurrent.futures
import json
from pathlib import Path
from typing import TypeAlias

import servicepathmapper.common.strings.file_names as file_names
import servicepathmapper.common.types.paths_type_hints as paths_types
from servicepathmapper.common.logger import Logger
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.exception_types.code_behavior_error import CodeBehaviorError
from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.io.output_generators.base import OutputGenerator


class FileSystemOutputGenerator(OutputGenerator):
    def __init__(self, out_dir_path: Path) -> None:
        _create_directory(out_dir_path, False)
        Logger.create_file_logger(out_dir_path / file_names.OUTPUT_LOG_FILE_NAME)

    def _generate_output(self, output_params: OutputGenerationParams) -> int:
        _output_stats(output_params)
        if not output_params.stats_only:
            if output_params.paths_by_servers_group_by_len is None:
                raise CodeBehaviorError(error='Paths is unexpectedly None!')
            _output_paths(output_params)
        return 0


def _output_stats(params: OutputGenerationParams) -> None:
    stats = params.config_stats
    if params.participation_counters is not None:
        stats.update(params.participation_counters)
    _write_stats(params.out_dir_path, stats, params.stats_in_dir)


def _write_stats(out_dir_path: Path, stats: dict, stats_in_dir: bool) -> None:
    if not stats_in_dir:
        _write_stats_in_single_file(out_dir_path, stats)
    else:
        _write_stats_in_dir(out_dir_path, stats)


def _write_stats_in_single_file(out_dir_path: Path, stats: dict) -> None:
    stats_file = out_dir_path / file_names.OUTPUT_STATS_FILE_NAME
    stats_file.write_text(json.dumps(stats, indent=4), encoding='utf-8')


def _write_stats_in_dir(out_dir_path: Path, stats: dict) -> None:
    stats_dir_path = out_dir_path / file_names.OUTPUT_STATS_DIR_NAME
    stats_dir_path.mkdir()
    for stat_key, stat_value in stats.items():
        stat_file = stats_dir_path / stat_key
        if stat_value:
            stat_file.write_text(json.dumps({stat_key: stat_value}, indent=4), encoding='utf-8')
        else:
            stat_file.touch()


def _output_paths(output_params: OutputGenerationParams) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=output_params.max_threads) as executor:
        futures = []
        for sz, groups_of_sz in enumerate(output_params.paths_by_servers_group_by_len):
            if groups_of_sz:
                output_dir = output_params.out_dir_path / f'{file_names.OUTPUT_FILE_NAME_PART_PATH_LEN}_{sz}'
                _create_directory(output_dir, True)
                for sequence_num, group_and_paths in enumerate(groups_of_sz.items()):
                    file_path = output_dir / str(sequence_num)
                    future = executor.submit(
                        _output_group,
                        entities=output_params.entities,
                        file_path=file_path,
                        group_and_paths=group_and_paths,
                        groups_only=output_params.server_groups_only,
                    )
                    future.file_path = file_path
                    futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                file_path = getattr(future, 'file_path', 'unknown')
                raise FileSystemError(
                    title='Failed to write file.',
                    values={'path': str(file_path), 'error': str(e)}
                )


def _output_group(
        entities: Entities,
        file_path: Path,
        group_and_paths: tuple[paths_types.ServersGroupId, list[paths_types.ServiceBasedPath]],
        groups_only: bool,
) -> None:
    group_members_ids_to_names = {
        server_id: entities.server_id_to_name[server_id] for server_id in group_and_paths[0]
    }
    _write_group_members(file_path, sorted(group_members_ids_to_names.values()))

    if not groups_only:
        formatted_paths = _group_paths_to_final_str(
            entities=entities,
            paths_of_group=group_and_paths[1],
            group_members_ids_to_names=group_members_ids_to_names,
        )
        _write_group_paths(file_path, formatted_paths)


def _write_group_members(file_path: Path, server_names: list[str]) -> None:
    group_file = file_path.with_name(file_path.name + '_' + file_names.OUTPUT_FILE_NAME_PART_SERVERS_GROUP)
    group_file.write_text('\n'.join(server_names), encoding='utf-8')


def _write_group_paths(file_path: Path, formatted_paths: str) -> None:
    file_path.write_text(formatted_paths, encoding='utf-8')


def _group_paths_to_final_str(
        entities: Entities,
        paths_of_group: list[paths_types.ServiceBasedPath],
        group_members_ids_to_names: dict[paths_types.ServerId, str]
) -> str:
    names_paths = [
        _ids_path_to_names_path(
            entities=entities,
            ids_path=path,
            group_members_ids_to_names=group_members_ids_to_names,
        )
        for path in paths_of_group
    ]
    return '\n'.join([_format_path_line(path) for path in names_paths])


_NamesPath: TypeAlias = list[tuple[str, list[str]]]


def _ids_path_to_names_path(
        entities: Entities,
        ids_path: paths_types.ServiceBasedPath,
        group_members_ids_to_names: dict[paths_types.ServerId, str]
) -> _NamesPath:
    names_path: _NamesPath = [(group_members_ids_to_names[ids_path[0][0]], [])]
    for idx in range(1, len(ids_path)):
        provider_name = group_members_ids_to_names[ids_path[idx][0]]
        names_path.append(
            (
                provider_name,
                sorted(
                    [
                        entities.service_id_to_name[service_id]
                        for service_id in ids_path[idx][1]
                    ]
                ),
            )
        )
    return names_path


def _create_directory(path: Path, exist_ok: bool = False) -> None:
    path.mkdir(parents=True, exist_ok=exist_ok)


def _format_path_line(names_path: _NamesPath) -> str:
    parts = [names_path[0][0]]
    for provider, services in names_path[1:]:
        services_str = ', '.join(services)
        parts.append(f'[{services_str}] {provider}')
    return ' '.join(parts)
