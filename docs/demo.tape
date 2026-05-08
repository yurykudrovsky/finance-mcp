# VHS Tape for finance-mcp terminal demo
# To generate the GIF, install vhs (https://github.com/charmbracelet/vhs) and run: vhs docs/demo.tape

Output docs/demo.gif
Require uv
Set FontSize 18
Set Width 1200
Set Height 800
Set TypingSpeed 50ms
Set Theme "Catppuccin Macchiato"

Type "uv run finance-mcp"
Enter
Sleep 2s
# Notice that the stdio server is running
Type "Waiting for MCP client connections..."
Sleep 1s
Ctrl+C

# Show a manual python script invoking the tool
Type "uv run python -c \"import asyncio; from finance_mcp.tools.quote import get_quote; print(asyncio.run(get_quote('AAPL')))\""
Enter
Sleep 3s
