from unittest.mock import patch, MagicMock

import pytest

import servicepathmapper.common.constants as constants
import servicepathmapper.common.constants as constants
from servicepathmapper.common.strings import program_args
from servicepathmapper.common.types.exception_types.safeguard_error import SafeguardError
from servicepathmapper.logic.validate_potential_for_paths import _validate_program_complexity


def make_args(force_large=False):
    return {program_args.ARG_FORCE_LARGE_COMPUTATION: force_large}


def test_validate_program_complexity_raises(monkeypatch):
    monkeypatch.setattr(
        'servicepathmapper.logic.validate_potential_for_paths._calc_complexity',
        lambda args, entities: constants.SAFEGUARD_THRESHOLD_COMPLEXITY + 1
    )
    args = make_args(force_large=False)
    entities = MagicMock()

    with pytest.raises(SafeguardError) as exc_info:
        _validate_program_complexity(args, entities)
    assert 'complexity exceeds safe limits' in exc_info.value.title
    assert exc_info.value.values.get('Safe complexity') == f'{constants.SAFEGUARD_THRESHOLD_COMPLEXITY:,}'
    assert exc_info.value.help_topics == [program_args.ARG_FORCE_LARGE_COMPUTATION]


def test_validate_program_complexity_warns(monkeypatch):
    monkeypatch.setattr(
        'servicepathmapper.logic.validate_potential_for_paths._calc_complexity',
        lambda args, entities: constants.SAFEGUARD_THRESHOLD_COMPLEXITY + 1
    )
    args = make_args(force_large=True)
    entities = MagicMock()

    with patch('servicepathmapper.common.logger.Logger.log') as mock_log:
        _validate_program_complexity(args, entities)
        assert mock_log.called
