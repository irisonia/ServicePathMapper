from servicepathmapper.io.output_generators.tests_capture import TestsCaptureOutputGenerator
from servicepathmapper.service_path_mapper import main
from ... import tests_strings as tests_common


def run_test_case_with_log_message(config: {},
                                   expected_values: {},
                                   expected_help_topics: [],
                                   expected_common_title: str,
                                   caplog) -> None:
    res = main(config, TestsCaptureOutputGenerator())
    assert not res.actual_results[tests_common.TESTS_OUTPUT_PATHS]

    log_text = caplog.text
    assert expected_common_title in log_text, f'Expected log message for '
    f'"{expected_common_title}" not found in log. log_test: {log_text}'

    missing_pairs = [f'{k}: {v}' for k, v in expected_values.items() if f'{k}: {v}' not in log_text]
    assert not missing_pairs, f'Missing value pairs in log: {missing_pairs}.  log_test: {log_text}'

    missing_topics = [f'--{topic}' for topic in expected_help_topics if f'--{topic}' not in log_text]
    assert not missing_topics, f'Missing help topics in log: {missing_topics}.  log_test: {log_text}'
