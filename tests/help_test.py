import precicecli.cli as cli
import pytest


HELP_ARGS = [
    ["-h"],
    ["config", "-h"],
    ["config", "check", "-h"],
    ["config", "format", "-h"],
    ["config", "visualize", "-h"],
    ["config", "doc", "-h"],
    ["profiling", "-h"],
    ["profiling", "merge", "-h"],
    ["profiling", "export", "-h"],
    ["profiling", "trace", "-h"],
    ["profiling", "analyze", "-h"],
    ["version", "-h"],
    ["init", "-h"],
]


@pytest.mark.parametrize("test_args", HELP_ARGS)
def test_help(test_args):
    print(f"Testing {test_args=}")
    parser, checker = cli.makeParser()
    with pytest.raises(SystemExit) as exc:
        ns = parser.parse_args(test_args)
        assert exc.value.code == 0
        assert checker(ns) == 0
