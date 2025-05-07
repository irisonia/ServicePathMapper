import logging

from servicepathmapper.io.output_generators.tests_dummy import DummyOutputGenerator
from servicepathmapper.service_path_mapper import main


def run_test_case(config: {}, expected_values: {}, expected_help_topics: [], caplog) -> None:
    caplog.set_level(logging.INFO)
    main(config, DummyOutputGenerator())

    for k, v in expected_values.items():
        assert f'{k}={v}' in caplog.text, f'Missing value pair: {k}={v} in log'

    for topic in expected_help_topics:
        assert f'--{topic}' in caplog.text, f'Missing help topic: --{topic} in log'
