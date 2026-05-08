# Contributing to finance-mcp

First off, thank you for considering contributing to `finance-mcp`! It's people like you that make open-source such a great community.

## Development Setup

We use `uv` for lightning-fast environment and dependency management.

1. **Install uv** (if you haven't already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yurykudrovsky/finance-mcp.git
   cd finance-mcp
   ```

3. **Install dependencies**:
   ```bash
   uv sync --dev
   ```

## Code Style

This project enforces strict code quality standards to ensure reliability.

- **Linting & Formatting**: We use `ruff`.
  ```bash
  uv run ruff check src/ tests/
  uv run ruff format src/ tests/
  ```

- **Type Checking**: We use `mypy` with `--strict` mode.
  ```bash
  uv run mypy --strict src/ tests/
  ```

## Running Tests

We use `pytest` for unit testing. Please ensure all tests pass before submitting a Pull Request, and include tests for any new features or bug fixes.

```bash
uv run pytest tests/
```

## Submitting a Pull Request

1. Fork the repository and create your branch from `main`.
2. Write clear, concise commit messages.
3. Ensure your code passes all CI checks (linting, type checking, and tests).
4. Open a Pull Request and describe the changes you've made. Link any relevant issues.

Thank you for your contributions!
