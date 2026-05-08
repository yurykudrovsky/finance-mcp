# Publishing to PyPI

When you are ready to publish `finance-mcp` to PyPI, follow these steps. Do not run these commands until you're absolutely ready to release.

1. **Ensure your environment is set up and working cleanly:**
   ```bash
   uv sync
   uv run pytest tests/
   ```

2. **Build the distributions (wheel and sdist):**
   ```bash
   uv build
   ```
   This will create a `dist/` directory with `.whl` and `.tar.gz` files.

3. **Publish to PyPI using uv:**
   ```bash
   uv publish
   ```
   You will be prompted for your PyPI API token (or username/password) unless configured via environment variables (e.g., `UV_PUBLISH_TOKEN`).

*(Note: Once published, verify the release at https://pypi.org/project/finance-mcp/)*
