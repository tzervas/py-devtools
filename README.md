# py-devtools

Suite of Python development utilities and project management tools with rich terminal interface.

## Installation

```bash
pip install py-devtools
```

## Usage

Initialize a new Python project:

```bash
devtools init --name my-project --template cli
```

Or run interactively:

```bash
devtools init --interactive
```

Check project status:

```bash
devtools status
```

Run common development commands:

```bash
devtools run test
devtools run lint
devtools run format
devtools run typecheck
devtools run clean
```

## Features

- **Project Initialization**: Create new Python projects with best practices
- **Status Monitoring**: Check project health and configuration
- **Command Runner**: Execute common development tasks with one command
- **Rich Interface**: Beautiful terminal output with colors and tables
- **Template Support**: Multiple project templates (basic, web, cli, lib)

## Templates

- **basic**: Minimal Python project structure
- **web**: Web application with FastAPI
- **cli**: Command-line application with Click
- **lib**: Python library with comprehensive tooling

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Format code
uv run black src/
uv run isort src/
```

## License

MIT License - see [LICENSE](LICENSE) for details.