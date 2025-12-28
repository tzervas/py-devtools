"""Command-line interface for Python development utilities."""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()


@click.group()
@click.version_option()
def main():
    """Python development utilities and project management tools."""
    pass


@main.command()
@click.option("--interactive", "-i", is_flag=True, help="Run in interactive mode")
@click.option("--name", "-n", help="Project name")
@click.option("--template", "-t", type=click.Choice(["basic", "web", "cli", "lib"]), default="basic")
def init(interactive, name, template):
    """Initialize a new Python project with best practices."""
    if interactive:
        name = name or questionary.text("Project name:").ask()
        template = template or questionary.select(
            "Project template:",
            choices=["basic", "web", "cli", "lib"],
            default="basic"
        ).ask()

    if not name:
        console.print("[red]Error: Project name is required[/red]")
        return 1

    project_path = Path.cwd() / name

    if project_path.exists():
        console.print(f"[red]Error: Directory {name} already exists[/red]")
        return 1

    console.print(f"[green]Creating Python project: {name}[/green]")
    console.print(f"[blue]Template: {template}[/blue]")

    # Create project structure
    project_path.mkdir()
    os.chdir(project_path)

    # Create basic structure
    (project_path / "src").mkdir()
    (project_path / "src" / name.replace("-", "_")).mkdir()
    (project_path / "tests").mkdir()

    # Create pyproject.toml
    pyproject_content = f'''[project]
name = "{name}"
version = "0.1.0"
description = "A Python project"
readme = "README.md"
requires-python = ">=3.9"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{name.replace("-", "_")}"]

[project.scripts]
{name.replace("-", "_")} = "{name.replace("-", "_")}.cli:main"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
]
'''

    with open(project_path / "pyproject.toml", "w") as f:
        f.write(pyproject_content)

    # Create basic files
    with open(project_path / "README.md", "w") as f:
        f.write(f"# {name}\n\nA Python project.\n")

    with open(project_path / "src" / name.replace("-", "_") / "__init__.py", "w") as f:
        f.write(f'"""Main package for {name}."""\n\n__version__ = "0.1.0"\n')

    with open(project_path / "src" / name.replace("-", "_") / "cli.py", "w") as f:
        f.write(f'''"""Command-line interface for {name}."""

import click


@click.group()
@click.version_option()
def main():
    """{name} command-line tool."""
    pass


@main.command()
def hello():
    """Say hello."""
    click.echo("Hello from {name}!")


if __name__ == "__main__":
    main()
''')

    with open(project_path / "tests" / "__init__.py", "w") as f:
        f.write("")

    with open(project_path / "tests" / "test_basic.py", "w") as f:
        f.write('''"""Basic tests."""

def test_example():
    """Example test."""
    assert True
''')

    console.print("[green]✅ Project initialized successfully![/green]")
    console.print(f"[blue]Next steps:[/blue]")
    console.print(f"  cd {name}")
    console.print("  uv sync --dev")
    console.print("  uv run pytest")


@main.command()
def status():
    """Show project status and health metrics."""
    console.print("[bold blue]Python Project Status[/bold blue]")

    # Check for common files
    files_to_check = [
        "pyproject.toml",
        "README.md",
        ".gitignore",
        "src/",
        "tests/",
    ]

    table = Table()
    table.add_column("File/Directory", style="cyan")
    table.add_column("Status", style="green")

    for file_path in files_to_check:
        exists = Path(file_path).exists()
        status = "[green]✓[/green]" if exists else "[red]✗[/red]"
        table.add_row(file_path, status)

    console.print(table)

    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    console.print(f"\n[blue]Python Version:[/blue] {python_version}")

    # Check if in virtual environment
    in_venv = sys.prefix != sys.base_prefix
    venv_status = "[green]Active[/green]" if in_venv else "[yellow]Not active[/yellow]"
    console.print(f"[blue]Virtual Environment:[/blue] {venv_status}")


@main.command()
@click.argument("command")
@click.option("--verbose", "-v", is_flag=True)
def run(command, verbose):
    """Run common development commands."""
    commands = {
        "test": ["pytest"],
        "lint": ["black", "--check", "src/", "tests/"],
        "format": ["black", "src/", "tests/"],
        "typecheck": ["mypy", "src/"],
        "clean": ["rm", "-rf", "__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache"],
    }

    if command not in commands:
        console.print(f"[red]Unknown command: {command}[/red]")
        console.print(f"[blue]Available commands: {', '.join(commands.keys())}[/blue]")
        return 1

    cmd = commands[command]
    if verbose:
        console.print(f"[blue]Running: {' '.join(cmd)}[/blue]")

    try:
        result = subprocess.run(cmd, capture_output=not verbose)
        if result.returncode == 0:
            console.print(f"[green]✅ {command} completed successfully[/green]")
        else:
            console.print(f"[red]❌ {command} failed[/red]")
            if not verbose:
                console.print(result.stderr.decode())
            return result.returncode
    except FileNotFoundError:
        console.print(f"[red]Command not found. Make sure dependencies are installed.[/red]")
        return 1


if __name__ == "__main__":
    main()