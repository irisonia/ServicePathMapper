"""
Aliases of paths types, for type hints only
"""

from collections import defaultdict
from typing import TypeAlias

ServerId: TypeAlias = int
ServiceId: TypeAlias = int
ServersGroupId: TypeAlias = frozenset[ServerId]
ServiceBasedPathNode: TypeAlias = tuple[ServerId, list[ServiceId]]
ServiceBasedPath: TypeAlias = list[ServiceBasedPathNode]
PathsByServersGroup: TypeAlias = defaultdict[ServersGroupId, list[ServiceBasedPath]]
PathsByServersGroupByLen: TypeAlias = list[PathsByServersGroup]
