"""Tests for devtools CLI."""

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from devtools.cli import main


def test_cli_help():
    """Test that CLI shows help."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Python development utilities" in result.output


def test_status_command():
    """Test status command."""
    runner = CliRunner()
    result = runner.invoke(main, ["status"])
    assert result.exit_code == 0
    assert "Python Project Status" in result.output


def test_run_command():
    """Test run command without recursively invoking real pytest."""
    runner = CliRunner()
    mock_result = MagicMock(returncode=0, stderr=b"")
    with patch("devtools.cli.subprocess.run", return_value=mock_result) as mock_run:
        result = runner.invoke(main, ["run", "test"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert mock_run.call_args.args[0] == ["pytest"]


def test_run_unknown_command():
    """Unknown run subcommands should fail cleanly."""
    runner = CliRunner()
    result = runner.invoke(main, ["run", "not-a-real-command"])
    assert result.exit_code == 1
    assert "Unknown command" in result.output
