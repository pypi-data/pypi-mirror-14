import pytest
import click
from click.testing import CliRunner


@pytest.mark.unit
def test_toplevel_cli():
    from tomb_cli.main import cli
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert '-h, --help' in result.output


@pytest.mark.unit
def test_subcommand_missing_app_cfg():
    from tomb_cli.main import cli

    @cli.command()
    @click.pass_context
    def hello(ctx):
        click.echo("Hello, Moon!")

    cli.add_command(hello)
    runner = CliRunner()
    result = runner.invoke(cli, ['hello'])
    assert result.exit_code == 1
    msg = 'app.yaml was not found, please create it or use -c'
    assert msg in result.output


@pytest.mark.unit
def test_subcommand_cli():
    from tomb_cli.main import cli

    @cli.command()
    @click.pass_context
    def hello(ctx):
        click.echo("Hello, Moon!")

    cli.add_command(hello)
    runner = CliRunner()
    result = runner.invoke(cli, ['-c', './tests/fixtures/complete_app.yaml',
                                 'hello'])
    assert result.exit_code == 0, result.output
    msg = 'Hello, Moon'
    assert msg in result.output
