import logging
import sys

import servicepathmapper.common.strings.help as program_help
import servicepathmapper.common.strings.program_args as program_args
import servicepathmapper.io.input.arg_info as arg_info
import tests.tests_strings as tests_common
from servicepathmapper.common.logger import Logger
from servicepathmapper.common.strings.about import PACKAGE_NAME
from servicepathmapper.common.types.config_stats import ConfigStats
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.participation_in_paths_counters import ParticipationInPathsCounters
from servicepathmapper.io.input.get_args import get_program_args
from servicepathmapper.io.input.process_args import process_program_args
from servicepathmapper.io.output_generators.base import OutputGenerator
from servicepathmapper.io.output_generators.file_system import FileSystemOutputGenerator
from servicepathmapper.logic.paths import map_paths


def main(test_config: dict = None, output_generator: OutputGenerator = None) -> int | dict:
    try:
        Logger.create_console_logger()

        config_args, help_args = get_program_args(test_config)
        _print_help(help_args)
        if help_args:
            return 0

        if output_generator is None:
            output_generator = FileSystemOutputGenerator(config_args[program_args.ARG_OUTPUT_DIR])

        Logger.log(_get_configuration_summary(config_args), logging.INFO)

        entities, config_stats = process_program_args(config_args)

        res = _run(entities=entities,
                   config_args=config_args,
                   config_stats=config_stats,
                   output_generator=output_generator)

        if test_config is not None:
            return {
                tests_common.TEST_RESULT_ENTITIES: entities,
                tests_common.TEST_RESULT_ACTUAL: res
            }

    except Exception as e:
        if test_config is not None:
            print(f'{str(e)}', file=sys.stderr)
            raise e

        try:
            Logger.log(f'{str(e)}', logging.ERROR)
        except Exception:
            pass
        return 1


def _print_help(help_args: set[str]) -> None:
    """Print the help message associated with each item in the given list of help subjects"""

    help_str_by_topic = {
        program_args.ARG_HELP_CONFIG: program_help.CONFIG_HELP_STR,
        program_args.ARG_HELP_OUTPUT: program_help.OUTPUT_HELP_STR,
        program_args.ARG_HELP_STATS: program_help.OUTPUT_STATS_HELP_STR,
        program_args.ARG_HELP_PATHS: program_help.OUTPUT_PATHS_HELP_STR
    }

    for help_topic in help_args:
        if help_topic in help_str_by_topic:
            print(help_str_by_topic[help_topic], '\n')


def _get_configuration_summary(args: dict) -> str:
    summary = f'{PACKAGE_NAME} is running with the following config:\n'
    for arg_key, arg_data in arg_info.ARG_INFO.items():
        metadata = arg_data.get(arg_info.ARG_METADATA, 0)
        if not (metadata & arg_info.ArgMetadata.HELP):
            if arg_key in args:
                summary += f'{arg_key:<15}: {args[arg_key]}\n'
            else:
                summary += f'{arg_key:<15}:\n'
    return summary


def _run(
        entities: Entities,
        config_args: dict,
        config_stats: ConfigStats,
        output_generator: OutputGenerator
) -> int | dict:
    paths = None
    participation_in_paths_counters = None
    if not config_args[program_args.ARG_CONFIG_STATS_ONLY]:
        paths = map_paths(
            entities=entities,
            src_server_name=str(config_args[program_args.ARG_SRC_SERVER]),
            dst_server_name=str(config_args[program_args.ARG_DST_SERVER]),
            min_path_len=config_args[program_args.ARG_MIN_PATH_LEN],
            max_path_len=config_args[program_args.ARG_MAX_PATH_LEN]
        )
        participation_in_paths_counters = ParticipationInPathsCounters(
            entities=entities,
            config_stats=config_stats,
            paths_by_servers_group_by_len=paths
        )

    return output_generator.generate_output(
        entities=entities,
        out_dir_path=config_args[program_args.ARG_OUTPUT_DIR],
        config_stats=config_stats,
        participation_counters=participation_in_paths_counters,
        paths_by_path_length_by_servers_group=paths,
        server_groups_only=config_args[program_args.ARG_SERVER_GROUPS_ONLY],
        stats_only=config_args[program_args.ARG_STATS_ONLY],
        max_threads=config_args[program_args.ARG_MAX_THREADS])


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
