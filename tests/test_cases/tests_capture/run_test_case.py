from typing import TypeAlias

from deepdiff import DeepDiff

from servicepathmapper.common.types.entities import Entities
from servicepathmapper.common.types.paths_type_hints import PathsByServersGroupByLen
from servicepathmapper.common.types.tests_capture import TestsCapture
from servicepathmapper.io.output_generators.tests_capture import TestsCaptureOutputGenerator
from servicepathmapper.service_path_mapper import main
from tests.tests_strings import TESTS_OUTPUT_PATHS, TESTS_OUTPUT_PARTICIPATION_CTRS, TESTS_OUTPUT_CONFIG_STATS


def run_test_case(config: dict, expected_results: dict) -> None:
    res: TestsCapture = main(config, TestsCaptureOutputGenerator())
    check_results_tests_capture(entities=res.entities, actual=res.actual_results, expected=expected_results)


def check_results_tests_capture(entities: Entities, actual: dict, expected: dict) -> None:
    assert actual is not None, 'Actual output is unexpectedly None'

    def compare_output(output_section, cmp_func, *args):
        field_in_expected = expected.get(output_section) is not None
        field_in_actual = actual.get(output_section) is not None
        if field_in_expected != field_in_actual:
            msg = (f'Actual output missing {output_section}'
                   if field_in_expected
                   else f'Actual output has an unexpected {output_section}')
            raise AssertionError(msg)
        if field_in_expected:
            cmp_func(actual[output_section], expected[output_section], *args)

    compare_output(TESTS_OUTPUT_CONFIG_STATS, _compare_config_stats)
    compare_output(TESTS_OUTPUT_PARTICIPATION_CTRS, _compare_participation_ctrs)
    compare_output(TESTS_OUTPUT_PATHS, _compare_paths, entities)


def _compare_config_stats(actual, expected) -> None:
    diff = DeepDiff(actual, expected, ignore_order=True)
    assert not diff, f'{TESTS_OUTPUT_CONFIG_STATS} differ:\nactual:\n{actual}\nexpected:\n{expected}'


def _compare_participation_ctrs(actual, expected) -> None:
    diff = DeepDiff(actual, expected, ignore_order=True)
    assert not diff, f'{TESTS_OUTPUT_PARTICIPATION_CTRS} differ:\nactual:\n{actual}\nexpected:\n{expected}'


_PathsByServersGroupWithNames: TypeAlias = dict[tuple[str, ...], list[list[tuple[str, list[str]]]]]


def _compare_paths(actual: PathsByServersGroupByLen,
                   expected: list[_PathsByServersGroupWithNames],
                   entities: Entities) -> None:
    assert len(actual) == len(expected), f'paths length differ: actual: {len(actual)}, expected: {len(expected)}'
    if not expected:
        return
    normalized_actual = _normalize_paths(entities, actual)
    assert normalized_actual == expected, f'paths differ: actual: {normalized_actual}, expected: {expected}'


def _normalize_paths(entities: Entities, paths_by_length_by_servers_group: PathsByServersGroupByLen
                     ) -> list[_PathsByServersGroupWithNames]:
    """
    Normalize actual paths for deterministic comparison with expected results in tests.
    """

    normalized: list[_PathsByServersGroupWithNames] = []

    for path_len in paths_by_length_by_servers_group:
        paths_by_group: _PathsByServersGroupWithNames = {}
        for group_members, group_paths in path_len.items():
            paths_with_names = []
            for path in group_paths:
                path_with_names = []
                for server_and_services_ids in path:
                    server_name = entities.server_id_to_name[server_and_services_ids[0]]
                    services_names = sorted(entities.service_id_to_name[id] for id in server_and_services_ids[1])
                    path_with_names.append((server_name, services_names))
                paths_with_names.append(path_with_names)
            servers_group_with_names = tuple(sorted(entities.server_id_to_name[id] for id in group_members))
            paths_by_group[servers_group_with_names] = sorted(paths_with_names)
        normalized.append(dict(sorted(paths_by_group.items())))
    return normalized
