# Building a Resilient Finance MCP Server

AI agents are only as smart as the data they can access. To turn Claude into a production-grade financial analyst, I built `finance-mcp`—an asynchronous, Python-powered Model Context Protocol (MCP) server that pipes live stock quotes, OHLCV history, and technical indicators directly into the LLM's context window. No API keys required, zero configuration, and sub-second latency.

## Why MCP?

Before MCP, giving an LLM access to real-world data meant wrestling with brittle, proprietary plugin architectures that broke with every upstream change. MCP standardizes this. By building an MCP server, I abstracted away HTTP requests and JSON parsing into a strict Pydantic schema that Claude natively understands.

Now, typing *"Compare AAPL and MSFT fundamentals"* prompts Claude to autonomously query the `compare_stocks` tool, ingest the Markdown payload, and synthesize the results instantly.

## Engineering Resilience: The DataProvider Pattern

A core design principle for `finance-mcp` was a seamless developer experience: clone, run, and go. While `yfinance` serves as an excellent zero-config primary engine, its reliance on undocumented endpoints introduces risk. 

To guarantee uptime, I implemented a robust `DataProvider` interface. If the primary source fails or hits a rate limit, the server seamlessly degrades to a secondary provider (like Alpha Vantage).

```python
class DataProvider:
    @staticmethod
    def get_quote(symbol: str) -> Quote:
        """Fetch quote using yfinance, seamlessly fallback to Alpha Vantage on failure."""
        try:
            return DataProvider._get_quote_yfinance(symbol)
        except Exception as e_yf:
            print(f"yfinance failed for {symbol}. Falling back to Alpha Vantage...")
            return DataProvider._get_quote_alphavantage(symbol)
```

The user never notices the disruption. Claude simply waits a few extra milliseconds, and the analysis continues flawlessly.

## Surviving the Throttling: The TTL Cache Strategy

LLMs are notoriously aggressive with tool usage. Claude will frequently query the same ticker multiple times in a single logical step to verify its own reasoning. Without a caching layer, upstream data providers would aggressively rate-limit the server.

To solve this, I engineered a lightweight, asynchronous Time-To-Live (TTL) cache directly into the tool layer using a custom Python decorator:

```python
def with_cache(ttl: float):
    """Decorator to cache tool responses and prevent upstream rate limits."""
    cache = TTLCache(ttl)
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            if cached := cache.get(key):
                return cached
            result = await func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator
```

Fast-moving data (like live quotes) receives a tight 60-second TTL, while slow-moving data (like P/E ratios) persists for an hour. This architecture enables the server to absorb hundreds of identical queries without generating redundant network requests.

## What's Next

Building `finance-mcp` reinforced a critical lesson: the bottleneck in agentic AI is no longer reasoning capabilities—it's tool quality. If an MCP server returns messy or inconsistent data, the LLM hallucinates. When it provides clean, strongly-typed JSON via Pydantic, the LLM feels like magic.

Next up, I plan to integrate real-time WebSocket streams and extend support to cryptocurrency markets.

Want to turn Claude into your personal quantitative analyst? Check out the [finance-mcp GitHub Repository](https://github.com/yurykudrovsky/finance-mcp). It's fully open-source, async from the ground up, and thoroughly tested. Contributions are welcome!
