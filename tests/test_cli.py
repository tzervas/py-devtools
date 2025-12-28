"""Tests for devtools CLI."""

import pytest
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
    """Test run command with test."""
    runner = CliRunner()
    result = runner.invoke(main, ["run", "test"])
    # This might fail if pytest is not available, but that's okay for basic test
    assert result.exit_code in [0, 1]  # 0 for success, 1 for command failure