# Building a Resilient Finance MCP Server

The Model Context Protocol (MCP) has opened the floodgates for making AI assistants genuinely useful. I've always wanted to query stock market fundamentals, compare tickers, and calculate RSI natively inside my chat with Claude Desktop. But I didn't want to wrestle with complex API authentications or constantly refreshing dashboard UI. That's why I built `finance-mcp`, an asynchronous, Python-powered MCP server that pipes financial data straight into the LLM context window.

## Why MCP?

Before MCP, extending an LLM meant writing dedicated plugin architectures or hard-coding API integrations that broke the moment an endpoint shifted. MCP standardizes this. By building an MCP server, I abstract away the messy world of HTTP requests and raw JSON parsing. I simply define a strict Pydantic schema for what Claude *can* do, and Claude natively understands the capabilities. 

If I type: *"Compare the fundamentals of AAPL vs MSFT"*, Claude instantly queries the `compare_stocks` tool on my server, reads the returned Markdown payload, and synthesizes it seamlessly.

## The DataProvider Fallback Pattern

One of the main goals for `finance-mcp` was ensuring users could clone the repo and run it instantly—no API keys required. I chose `yfinance` as the primary engine. It aggressively scrapes Yahoo Finance and works right out of the box.

However, `yfinance` relies on undocumented endpoints. If Yahoo updates its frontend, the library can temporarily break. To engineer resilience, I implemented a `DataProvider` pattern. The server attempts to fetch from `yfinance`, and if it hits an exception, it seamlessly falls back to a secondary provider (like Alpha Vantage) via a generic interface. 

The user never notices the disruption. Claude simply waits a few extra milliseconds.

## Surviving the Throttling: The TTL Cache Strategy

LLMs are notoriously chatty. Sometimes Claude will query the same stock ticker three times in a single logical reasoning step to double-check its own math. Without a caching layer, `yfinance` would get rate-limited instantly.

I built a lightweight, asynchronous TTL (Time-To-Live) cache directly into the tool layer. Fast-moving data (like stock quotes) gets a 60-second TTL. Slow-moving data (like market cap or P/E ratio) gets a generous 1-hour TTL. By wrapping the cache around the tool handler, the MCP server can absorb hundreds of identical queries without ever pinging the upstream data source twice. 

## What I Learned

Building this taught me that the bottleneck in agentic AI is no longer the LLM's reasoning—it's the quality of the tools we provide. If an MCP server returns messy data, the LLM hallucinates. If it returns clean, strongly-typed JSON via Pydantic, the LLM feels magical. 

You can check out `finance-mcp` on my GitHub. It's fully open-source, async from the ground up, and thoroughly tested. Give it a try, and let Claude be your personal financial analyst.
