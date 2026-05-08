# Claude Desktop Demo Recording Script

Use this script to record the `demo.gif` showcasing `finance-mcp` working inside Claude Desktop. Total recording time should be around 30 seconds.

## Setup
1. Ensure the `finance-mcp` is correctly configured in your `claude_desktop_config.json`.
2. Start Claude Desktop and clear any previous conversation.
3. Start a screen recorder (like CleanShot X, Loom, or macOS built-in recorder) targeting the Claude Desktop window.

## Recording Script

1. **Start Recording**

2. **Prompt 1 (Data Fetch):**
   *Type:* "What is the current stock price and trading volume for AAPL?"
   *Wait for Claude to use the `get_quote` tool and answer.*

3. **Prompt 2 (Comparison):**
   *Type:* "Can you compare the fundamentals of AAPL vs MSFT?"
   *Wait for Claude to use the `compare_stocks` tool (or `get_fundamentals` twice) and output the comparison table.*

4. **Prompt 3 (Indicators):**
   *Type:* "What is the RSI for TSLA right now?"
   *Wait for Claude to use the `calc_indicators` tool.*

5. **Prompt 4 (History):**
   *Type:* "Pull the 1-month historical OHLCV data for NVDA."
   *Wait for Claude to use the `get_history` tool.*

6. **Prompt 5 (Follow-up):**
   *Type:* "Based on NVDA's recent history, how has it trended?"
   *Wait for the final analysis.*

7. **Stop Recording**

8. Export as `demo.gif` or `.mp4` and place it in the `docs/` directory.
