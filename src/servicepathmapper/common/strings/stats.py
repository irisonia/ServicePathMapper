OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS = 'services_having_clients_but_no_providers'
OUTPUT_STATS_SERVICES_HAVING_CLIENTS_BUT_NO_PROVIDERS_HELP_STR = (
    'Services found in files in the clients directory, but not in the providers directory.'
    '\nSorted by the number of servers being clients of the service, descending, then by service name, ascending.')
OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS = 'services_having_providers_but_no_clients'
OUTPUT_STATS_SERVICES_HAVING_PROVIDERS_BUT_NO_CLIENTS_HELP_STR = (
    'Services found in files in the providers directory, but not in the clients directory.'
    '\nSorted by the number of servers providing the service, descending, then by service name, ascending.')
OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT = 'services_unreachable_for_sole_provider_client'
OUTPUT_STATS_SERVICES_UNREACHABLE_FOR_SOLE_PROVIDER_CLIENT_HELP_STR = (
    'When a server is both the sole client and the sole provider of a specific service.'
    '\nBoth the servers and their services are sorted by name, ascending.')
OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVERS = 'actual_non_participating_servers'
OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVERS_HELP_STR = (
    'Following paths creations, the servers that do not participate in any path.'
    '\nSorted by server name, ascending.')
OUTPUT_STATS_ACTUAL_SERVER_PARTICIPATION_CTR = 'actual_server_participation_counters'
OUTPUT_STATS_ACTUAL_SERVER_PARTICIPATION_CTR_HELP_STR = (
    'For each server that participates in paths: '
    '\n-The number of server groups in which it participates (a servers group can make one or more paths).'
    '\n-The number of paths in which it participates.'
    '\nSorted by number of server groups in which the server participates, descending, then by the '
    '\nnumber of paths in which it participates, descending, then by server name, ascending.')
OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVICES = 'actual_non_participating_services'
OUTPUT_STATS_ACTUAL_NON_PARTICIPATING_SERVICES_HELP_STR = (
    'Services that are allowed to participate in paths and have both providers and clients,'
    '\nyet do not participate in any of the resulting paths. (Example for a reason: Servers'
    '\nthat are clients for a service can only join the path after the max_len of paths is passed).'
    '\nSorted by service name, ascending.')
OUTPUT_STATS_ACTUAL_SERVICE_PARTICIPATION_CTR = 'actual_service_participation_counters'
OUTPUT_STATS_ACTUAL_SERVICE_PARTICIPATION_CTR_HELP_STR = (
    'For each service that participates in paths, the number of paths in which it participates.'
    '\nSorted by number of paths in which the service participates, descending, then by service name, ascending.')
OUTPUT_STATS_ACTUAL_SERVER_PAIR_ADJACENCY_CTR = 'actual_server_pair_adjacency_counters'
OUTPUT_STATS_ACTUAL_SERVER_PAIR_ADJACENCY_CTR_HELP_STR = (
    'For every pair of servers with an edge in any of the resulting paths, '
    'the number of paths in which they have an edge.'
    '\nSorted by number of edges between the two servers, descending, then by server name, ascending.')

OUTPUT_STATS_PROVIDERS = 'providers'
OUTPUT_STATS_CLIENTS = 'clients'
OUTPUT_STATS_PROVIDERS_COUNTER = OUTPUT_STATS_PROVIDERS + '_count'
OUTPUT_STATS_CLIENTS_COUNTER = OUTPUT_STATS_CLIENTS + '_count'
OUTPUT_STATS_PARTICIPATION_COUNTER_ADJACENCY = 'adjacency_count'
OUTPUT_STATS_PARTICIPATION_COUNTER_PATHS = 'paths_count'
OUTPUT_STATS_PARTICIPATION_COUNTER_GROUPS = 'groups_count'
OUTPUT_STATS_SERVICE = 'service'
OUTPUT_STATS_SERVICES = 'services'
OUTPUT_STATS_SERVER = 'server'
OUTPUT_STATS_ADJACENT_SERVERS = 'adjacent_servers'
