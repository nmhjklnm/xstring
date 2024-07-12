"""Test cmdline"""
from __future__ import annotations  # PEP 585

import pytest
from click.testing import CliRunner

from xstring import __version__
from xstring.cmdline import main


@pytest.fixture
def clicker() -> CliRunner:
    return CliRunner()

@pytest.mark.parametrize(
    ['invoke_args', 'exit_code', 'output_keyword'],
    [
        ([], 0, 'help'),
        (['--help'], 0, 'help'),
        (['--version'], 0, __version__),
        (['-V'], 0, __version__),
    ]
)
def test_main(
        clicker: CliRunner,
        invoke_args: list[str],
        exit_code: int,
        output_keyword: str,
):
    """Test main cmdline"""
    result = clicker.invoke(main, invoke_args)
    assert result.exit_code == exit_code
    assert output_keyword in result.output

# @pytest.mark.parametrize(
#     ['invoke_args', 'exit_code', 'output_keyword'],
#     [
#         (['run', 'LazyLLM'], 0, 'Running with lazyllm'),
#         (['run', 'LazyLLM', '--pattern', 'fill'], 0, 'Running with lazyllm'),
#         (['run', 'LazyLLM/lazyllm', '--skip-modules', 'lazyllm.components.deploy.relay.server'], 0, 'Running with lazyllm'),
#     ]
# )
# def test_run_command(
#         clicker: CliRunner,
#         lazyllm_package,
#         invoke_args: list[str],
#         exit_code: int,
#         output_keyword: str,
# ):
#     """Test run command"""
#     result = clicker.invoke(main, invoke_args)
#     assert result.exit_code == exit_code
#     assert output_keyword in result.output
#     assert 'Run completed successfully.' in result.output
