from collections import defaultdict

import servicepathmapper.common.strings.stats as stats_strings
from servicepathmapper.common.types.entities import Entities


class ConfigStats:
    """
    statistics deduced from the configuration input, independent of mapping any paths.
    """

    def __init__(self):
        self.services_with_clients_no_providers_names = defaultdict(list)
        self.services_with_providers_no_clients = defaultdict(list)
        self.services_unreachable_for_sole_provider_client = defaultdict(list)

    def to_json(self, entities: Entities) -> dict:
        return {
            stats_strings.OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS: sorted(
                [
                    {
                        stats_strings.OUTPUT_STATS_SERVICE: item[0],
                        stats_strings.OUTPUT_STATS_CLIENTS_COUNTER: len(item[1]),
                        stats_strings.OUTPUT_STATS_CLIENTS: sorted([client for client in item[1]])
                    }
                    for item in self.services_with_clients_no_providers_names.items()
                ],
                key=lambda item: (-item[stats_strings.OUTPUT_STATS_CLIENTS_COUNTER],
                                  item[stats_strings.OUTPUT_STATS_SERVICE])
            ),
            stats_strings.OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS: sorted(
                [
                    {
                        stats_strings.OUTPUT_STATS_SERVICE: entities.service_id_to_name[item[0]],
                        stats_strings.OUTPUT_STATS_PROVIDERS_COUNTER: len(item[1]),
                        stats_strings.OUTPUT_STATS_PROVIDERS: sorted(
                            entities.server_id_to_name[provider] for provider in item[1]
                        )
                    }
                    for item in self.services_with_providers_no_clients.items()
                ],
                key=lambda item: (-item[stats_strings.OUTPUT_STATS_PROVIDERS_COUNTER],
                                  item[stats_strings.OUTPUT_STATS_SERVICE]),
            ),
            stats_strings.OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT: sorted(
                [
                    {
                        stats_strings.OUTPUT_STATS_SERVER: entities.server_id_to_name[item[0]],
                        stats_strings.OUTPUT_STATS_SERVICES: sorted(
                            [entities.service_id_to_name[key] for key in item[1]]
                        )
                    }
                    for item in self.services_unreachable_for_sole_provider_client.items()
                ],
                key=lambda item: (-len(item[stats_strings.OUTPUT_STATS_SERVICES]),
                                  item[stats_strings.OUTPUT_STATS_SERVER]),
            )
        }
