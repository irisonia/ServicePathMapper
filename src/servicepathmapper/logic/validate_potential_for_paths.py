import logging
import math

import servicepathmapper.common.constants as constants
from servicepathmapper.common.logger import Logger
from servicepathmapper.common.strings import program_args
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.exception_types.safeguard_error import SafeguardError
from servicepathmapper.common.types.runtime_messages import EarlyDetectNoPaths


def validate_potential_for_paths(args: dict, entities: Entities) -> bool:
    # validations that also need to raise
    _validate_program_complexity(args, entities)

    # regular validations
    return all(
        [_validate_enough_servers_for_min_path_len(entities, args[program_args.ARG_MIN_PATH_LEN]),
         _validate_mandatory_servers_may_participate(entities),
         _validate_mandatory_services_may_participate(entities)]
    )


def _validate_program_complexity(args: dict, entities: Entities) -> bool:
    """Warn or block execution if estimated computation exceeds safe complexity thresholds."""

    complexity = _calc_complexity(args, entities)
    if complexity > constants.SAFEGUARD_THRESHOLD_COMPLEXITY:
        force = args[program_args.ARG_FORCE_LARGE_COMPUTATION]
        force_str = '' if not force else f' Ignored due to flag {program_args.ARG_FORCE_LARGE_COMPUTATION}'
        error = SafeguardError(
            title=f'Predicted complexity exceeds safe limits!{force_str}',
            values={
                'Predicted complexity': f'{complexity:,}',
                'Safe complexity': f'{constants.SAFEGUARD_THRESHOLD_COMPLEXITY:,}'
            },
            help_topics=[program_args.ARG_FORCE_LARGE_COMPUTATION])
        Logger.log(str(error), level=logging.WARNING if force else logging.ERROR)

        if not force:
            raise error
        return False
    return True


def _calc_complexity(args: dict, entities: Entities) -> int:
    complexity = 0
    min_len = args[program_args.ARG_MIN_PATH_LEN]
    max_len = args[program_args.ARG_MAX_PATH_LEN]
    max_threads = args[program_args.ARG_MAX_THREADS]
    num_servers = len(entities.server_id_to_name)

    for path_len in range(min_len, max_len + 1):
        combinations = math.comb(num_servers - 2, path_len - 2)
        complexity += combinations / (max_threads * path_len)

    return math.ceil(complexity)


def _validate_enough_servers_for_min_path_len(entities: Entities, min_path_len: int) -> bool:
    """Early detect not having enough servers to create a path of the required minimal length."""

    total_servers = len(entities.server_name_to_id)
    if total_servers < min_path_len:
        Logger.log(str(
            EarlyDetectNoPaths(
                title=f'Not enough servers for {program_args.ARG_MIN_PATH_LEN}.',
                values={'servers': total_servers, program_args.ARG_MIN_PATH_LEN: min_path_len},
                help_topics=[program_args.ARG_MIN_PATH_LEN])),
            level=logging.INFO)
        return False
    return True


def _validate_mandatory_services_may_participate(entities: Entities) -> bool:
    """Early detect a required service unable to participate in paths."""

    services = [s for s in entities.mandatory_services_names if s not in entities.service_name_to_id]
    if services:
        Logger.log(str(
            EarlyDetectNoPaths(
                title="Mandatory services cannot participate.",
                values={'services': ', '.join(f'"{s}"' for s in services)},
                help_topics=[program_args.ARG_MANDATORY_SERVICES])),
            level=logging.INFO)
        return False
    return True


def _validate_mandatory_servers_may_participate(entities: Entities) -> bool:
    """Early detect a required server unable to participate in paths."""

    servers = [s for s in entities.mandatory_servers_names if s not in entities.server_name_to_id]
    if servers:
        Logger.log(str(
            EarlyDetectNoPaths(
                title="Mandatory servers cannot participate.",
                values={'servers': ', '.join(f'"{s}"' for s in servers)},
                help_topics=[program_args.ARG_MANDATORY_SERVERS])),
            level=logging.INFO)
        return False
    return True
