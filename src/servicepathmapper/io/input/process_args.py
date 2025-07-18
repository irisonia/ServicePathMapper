import logging
import math
from collections import defaultdict
from pathlib import Path

import servicepathmapper.common.constants as constants
import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.common.logger import Logger
from servicepathmapper.common.types.config_stats import ConfigStats
from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.exception_types.filesystem_error import FileSystemError
from servicepathmapper.common.types.exception_types.logic_error import LogicError
from servicepathmapper.common.types.exception_types.safeguard_error import SafeguardError


def process_program_args(args: dict) -> tuple[Entities, ConfigStats]:
    """
    Analyze and process program arguments into entities and their relationships.

    Args:
        args: Combined arguments from command-line, config file, and hard coded.

    Returns:
        tuple[Entities, ConfigStats].

    Raises:
        LogicError, for logical inconsistency (example: a server that is both mandatory and forbidden).
    """

    entities = Entities()
    _read_policy_files(args, entities)
    _set_hardcoded_config(args, entities)
    providers, clients = _init_servers(args, entities)
    config_stats = _set_relationships(args=args,
                                      entities=entities,
                                      providers=providers,
                                      clients=clients)
    _validate(args, entities)

    return entities, config_stats


def _read_lines_from_file(file_path: Path) -> set[str]:
    """:return: The lines from a file as a set of str."""

    try:
        content = file_path.read_text(encoding='utf-8')
        return {line.strip() for line in content.splitlines() if line.strip()}
    except (OSError, UnicodeDecodeError) as e:
        raise FileSystemError(
            title='Failed reading file',
            values={'path': str(file_path), 'error': str(e)}
        ) from e


def _read_policy_files(args: dict, entities: Entities) -> None:
    """Read from configuration policy files: mandatory, allowed and forbidden servers and services."""

    if program_args.ARG_MANDATORY_SERVERS in args:
        entities.mandatory_servers_names = _read_lines_from_file(args[program_args.ARG_MANDATORY_SERVERS])
    if program_args.ARG_ALLOWED_SERVERS in args:
        entities.allowed_servers_names = _read_lines_from_file(args[program_args.ARG_ALLOWED_SERVERS])
    elif program_args.ARG_FORBIDDEN_SERVERS in args:
        entities.forbidden_servers_names = _read_lines_from_file(args[program_args.ARG_FORBIDDEN_SERVERS])
    if program_args.ARG_MANDATORY_SERVICES in args:
        entities.mandatory_services_names = _read_lines_from_file(args[program_args.ARG_MANDATORY_SERVICES])
    if program_args.ARG_ALLOWED_SERVICES in args:
        entities.allowed_services_names = _read_lines_from_file(args[program_args.ARG_ALLOWED_SERVICES])
    elif program_args.ARG_FORBIDDEN_SERVICES in args:
        entities.forbidden_services_names = _read_lines_from_file(args[program_args.ARG_FORBIDDEN_SERVICES])


def _set_hardcoded_config(args: dict, entities: Entities) -> None:
    """Set config data that is fixed by the program."""

    entities.mandatory_servers_names.add(str(args[program_args.ARG_SRC_SERVER]))
    entities.mandatory_servers_names.add(str(args[program_args.ARG_DST_SERVER]))


def _init_servers(args: dict, entities: Entities) -> tuple[list[str], list[str]]:
    """
    Assign a unique id to every server that is allowed to participate.
    :return: list of providers files and list of clients files.
    """

    provider_dir = Path(args[program_args.ARG_PROVIDERS_DIR])
    providers = [f.name for f in provider_dir.iterdir() if f.is_file()]
    client_dir = Path(args[program_args.ARG_CLIENTS_DIR])
    clients = [f.name for f in client_dir.iterdir() if f.is_file()]

    for server_name in set(providers + clients):
        if _is_allowed(name=server_name,
                       mandatory=entities.mandatory_servers_names,
                       allowed=entities.allowed_servers_names,
                       forbidden=entities.forbidden_servers_names) \
                and (server_name not in entities.server_name_to_id):
            entities.server_id_to_name.append(server_name)
            entities.server_name_to_id[server_name] = len(entities.server_id_to_name) - 1

    providers = [p for p in providers if p in entities.server_name_to_id]
    clients = [c for c in clients if c in entities.server_name_to_id]
    return providers, clients


def _set_relationships(args: dict,
                       entities: Entities,
                       providers: list,
                       clients: list) -> ConfigStats:
    """Init client-provider relationships between servers-servers and servers-services."""

    config_stats = ConfigStats()

    for provider in providers:
        services = _read_lines_from_file(args[program_args.ARG_PROVIDERS_DIR] / provider)
        _init_services_for_provider(entities=entities, server_name=provider, service_names=services)

    for client in clients:
        services = _read_lines_from_file(args[program_args.ARG_CLIENTS_DIR] / client)
        _init_services_for_client(entities=entities,
                                  server_name=client,
                                  service_names=services,
                                  services_with_clients_no_providers=config_stats._services_with_clients_no_providers)

    config_stats._services_unreachable_for_sole_provider_client = (
        _init_services_unreachable_for_sole_provider_client(entities))
    config_stats._services_with_providers_no_clients = (
        config_stats).services_provided_but_with_no_clients = _init_services_provided_but_with_no_clients(entities)
    _init_providers_per_client(entities)

    return config_stats


def _init_services_for_provider(entities: Entities, server_name: str, service_names: set) -> None:
    """A callback. Gather all services provided by a server, and all servers providing a service."""

    server_id = entities.server_name_to_id[server_name]
    for service_name in service_names:
        if _is_allowed(name=service_name,
                       mandatory=entities.mandatory_services_names,
                       allowed=entities.allowed_services_names,
                       forbidden=entities.forbidden_services_names):
            if service_name not in entities.service_name_to_id:
                entities.service_id_to_name.append(service_name)
                entities.service_name_to_id[service_name] = len(entities.service_id_to_name) - 1
            service_id = entities.service_name_to_id[service_name]
            entities.providers_of_service[service_id].add(server_id)
            entities.services_of_provider[server_id].add(service_id)


def _init_services_for_client(entities: Entities,
                              server_name: str,
                              service_names: set,
                              services_with_clients_no_providers: defaultdict[str, list]) -> None:
    """A callback. Gather all servers being clients of a service, and all services to which a server is a client."""

    server_id = entities.server_name_to_id[server_name]

    for service_name in service_names:
        if service_name in entities.service_name_to_id:  # as _init_services_provided_by_server already placed it
            service_id = entities.service_name_to_id[service_name]
            entities.services_of_client[server_id].add(service_id)
            entities.clients_of_service[service_id].add(server_id)
        else:
            if _is_allowed(name=service_name,
                           mandatory=entities.mandatory_services_names,
                           allowed=entities.allowed_services_names,
                           forbidden=entities.forbidden_services_names):
                services_with_clients_no_providers[service_name].append(server_name)


def _is_allowed(name: str, mandatory: set, allowed: set, forbidden: set) -> bool:
    """
    Checks if an entity (server or service) may participate.
    :param name: Name of the entity.
    :param mandatory: Collection of mandatory entities. A mandatory entity is implicitly allowed.
    :param allowed: Collection of allowed entities.
    :param forbidden: Collection of forbidden entities.
    :return: True if the entity is allowed.
    """

    if len(allowed) != 0:
        return (name in allowed) or (name in mandatory)
    return name not in forbidden


def _init_services_unreachable_for_sole_provider_client(entities: Entities) -> defaultdict[str, list]:
    """A service where its sole provider is also its sole client."""
    services_unreachable_for_sole_provider_client = defaultdict(list)

    for service, providers in entities.providers_of_service.items():
        if (len(providers) == 1) and (providers == entities.clients_of_service[service]):
            p, = providers
            services_unreachable_for_sole_provider_client[p].append(service)

    return services_unreachable_for_sole_provider_client


def _init_services_provided_but_with_no_clients(entities: Entities) -> defaultdict[str, list]:
    """Find any service that has allowed providers, but no allowed clients."""
    services_with_providers_no_clients = defaultdict(list)

    for service_id in entities.providers_of_service:
        if ((service_id not in entities.clients_of_service)
                or (len(entities.clients_of_service[service_id]) == 0)):
            services_with_providers_no_clients[service_id] = sorted(
                p for p in entities.providers_of_service[service_id])

    return services_with_providers_no_clients


def _init_providers_per_client(entities: Entities) -> None:
    """Per client, gather all providers that provide any services it is a client of."""

    for client_id, services in entities.services_of_client.items():
        for service_id in services:
            for provider_id in entities.providers_of_service[service_id]:
                if provider_id != client_id:
                    entities.providers_of_client[client_id].add(provider_id)


def _validate(args: dict, entities: Entities) -> None:
    """
    Perform validations on the processed data.
    :raises LogicError: For logical inconsistency (example: a server that is both mandatory and forbidden)
    """

    _assert_disjoint(title_type='server',
                     first=entities.mandatory_servers_names,
                     second=entities.forbidden_servers_names,
                     title_first='mandatory servers',
                     title_second='forbidden servers')
    _assert_disjoint(title_type='service',
                     first=entities.mandatory_services_names,
                     second=entities.forbidden_services_names,
                     title_first='mandatory services',
                     title_second='forbidden services')

    _validate_program_complexity(args=args, entities=entities)


def _assert_disjoint(title_type: str, first: set, second: set, title_first: str, title_second: str) -> None:
    """Assert two containers have no elements in common."""

    if not first.isdisjoint(second):
        raise LogicError(title=f'{title_first} and {title_second} must not have any elements in common',
                         values={title_type: sorted(first & second)})


def _validate_program_complexity(args: dict, entities: Entities) -> None:
    """Warn or block if estimated computation exceeds safe complexity thresholds."""

    complexity = _calc_complexity(args, entities)
    if complexity > constants.SAFEGUARD_THRESHOLD_COMPLEXITY:
        if args[program_args.ARG_FORCE_LARGE_COMPUTATION]:
            Logger.log(str(
                SafeguardError(
                    title=f'Predicted complexity exceeds safe limits!',
                    values={
                        'Predicted complexity': f'{complexity:,}',
                        'Safe complexity': f'{constants.SAFEGUARD_THRESHOLD_COMPLEXITY:,}'
                    },
                    help_topics=[program_args.ARG_FORCE_LARGE_COMPUTATION])),
                level=logging.WARNING)
        else:
            raise SafeguardError(
                title='Predicted complexity exceeds safe limits.',
                values={
                    'Predicted complexity': f'{complexity:,}',
                    'Safe complexity': f'{constants.SAFEGUARD_THRESHOLD_COMPLEXITY:,}'
                },
                help_topics=[program_args.ARG_FORCE_LARGE_COMPUTATION]
            )


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
