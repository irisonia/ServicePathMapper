from collections import defaultdict

from servicepathmapper.common.types.config_stats import ConfigStats
from servicepathmapper.common.types.entities import Entities


def make_config_stats(entities: Entities,
                      services_with_clients_no_providers: defaultdict[str, list]) -> ConfigStats:
    config_stats = ConfigStats()
    config_stats._services_with_clients_no_providers = services_with_clients_no_providers
    config_stats._services_unreachable_for_sole_provider_client = (
        _init_services_unreachable_for_sole_provider_client(entities))
    config_stats._services_with_providers_no_clients = _init_services_provided_but_with_no_clients(entities)

    return config_stats


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
