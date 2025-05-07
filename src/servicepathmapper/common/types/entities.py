from collections import defaultdict


class Entities:
    """
    - Servers and services name-id mappings.
    - Servers and services that are mandatory/allowed/forbidden.
    - Server-server and server-services relationships.
    """

    def __init__(self):
        self.server_name_to_id = defaultdict(int)
        self.server_id_to_name = []

        self.service_name_to_id = defaultdict(int)
        self.service_id_to_name = []

        self.services_of_provider = defaultdict(set)
        self.providers_of_service = defaultdict(set)

        self.services_of_client = defaultdict(set)
        self.clients_of_service = defaultdict(set)

        self.providers_of_client = defaultdict(set)

        self.mandatory_servers_names = set()
        self.allowed_servers_names = set()
        self.forbidden_servers_names = set()

        self.mandatory_services_names = set()
        self.allowed_services_names = set()
        self.forbidden_services_names = set()
