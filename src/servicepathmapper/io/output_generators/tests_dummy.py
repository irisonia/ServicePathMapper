from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.io.output_generators.base import OutputGenerator


class DummyOutputGenerator(OutputGenerator):
    def _generate_output(self, params: OutputGenerationParams) -> int:
        return 0
