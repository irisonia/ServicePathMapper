import servicepathmapper.common.strings.program_args as program_args
from servicepathmapper.io.input.get_args import _categorize_args


def test_ignore_unrecognized_args(monkeypatch):
    args = {
        program_args.ARG_CLIENTS_DIR: 'clients',
        'unrecognized_field': 'should_be_ignored'
    }

    config_args, help_args = _categorize_args(args)
    assert program_args.ARG_CLIENTS_DIR in config_args
    assert str(config_args[program_args.ARG_CLIENTS_DIR]) == 'clients'
    assert 'unrecognized_field' not in config_args
    assert help_args == set()
