from dataclasses import dataclass

from servicepathmapper.common.types.entities import Entities


@dataclass
class TestsCapture:
    entities: Entities
    actual_results: {}
