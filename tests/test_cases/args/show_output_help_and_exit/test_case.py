from servicepathmapper.common.strings.help import OUTPUT_HELP_STR
from servicepathmapper.service_path_mapper import main


def test_show_output_help_and_exit(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['prog', '--help-output'])
    ret = main()
    assert ret == 0

    out, err = capsys.readouterr()
    assert OUTPUT_HELP_STR in out
    assert err == ""
