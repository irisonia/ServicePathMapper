from servicepathmapper.common.types.output_generation_params import OutputGenerationParams
from servicepathmapper.io.output_generators.base import OutputGenerator

import tests.tests_strings as tests_common


class TestsCaptureOutputGenerator(OutputGenerator):
    def _generate_output(self, output_params: OutputGenerationParams) -> dict:
        ret = dict()
        ret[tests_common.TESTS_OUTPUT_CONFIG_STATS] = output_params.config_stats
        if output_params.participation_counters:
            ret[tests_common.TESTS_OUTPUT_PARTICIPATION_CTRS] = output_params.participation_counters
        if not output_params.stats_only:
            ret[tests_common.TESTS_OUTPUT_PATHS] = output_params.paths_by_servers_group_by_len
        return ret
