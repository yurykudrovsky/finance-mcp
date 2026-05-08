# LinkedIn Post Variants

## Variant A: Technical angle (architecture decisions, fallback pattern, caching)

Ever noticed how brittle AI agents become when they hit undocumented APIs? 

I wanted Claude to be my personal quant, but throwing raw data at an LLM is a recipe for hallucinations. That’s why I built **finance-mcp**—an open-source, asynchronous Model Context Protocol (MCP) server that pipes live stock quotes, OHLCV history, and technical indicators directly into the context window.

To make it production-grade, I focused on two things:
1️⃣ **Resilience:** Built a generic DataProvider interface. If `yfinance` fails or rate-limits, it seamlessly falls back to Alpha Vantage.
2️⃣ **Caching:** LLMs query identical data frequently to verify their reasoning. I engineered a lightweight, async TTL cache right into the tool layer to absorb redundant calls and prevent upstream throttling.

Result? Clean, strongly-typed Pydantic JSON that makes the LLM feel like magic. 

Check out the code and the fallback patterns here:
🔗 https://github.com/yurykudrovsky/finance-mcp

#MCP #Python #Claude #AI #SoftwareEngineering

---

## Variant B: Builder angle (shipped a thing, here's the demo, here's the repo)

I built an AI tool that turns Claude Desktop into a real-time quantitative analyst. 📈

Over the weekend, I shipped **finance-mcp**. It’s an open-source server that uses the new Model Context Protocol (MCP) to give AI agents native, live access to financial markets. No API keys required, zero configuration, and sub-second latency.

You can ask Claude: *"Compare the fundamentals of AAPL vs MSFT and show me the RSI for TSLA"* and it autonomously queries the data, ingests the metrics, and synthesizes a full financial report. 

I designed it to be as frictionless as possible: just clone the repo and run it. It’s fully async, strictly typed with Pydantic, and thoroughly tested. 

If you want to play around with giving LLMs access to live market data, give it a spin!

🔗 Repo & Demo: https://github.com/yurykudrovsky/finance-mcp

#BuildInPublic #AI #OpenSource #Python #Finance

---

## Variant C: AI-ecosystem angle (MCP is the new plugin layer, here's a real example)

The Model Context Protocol (MCP) is quietly revolutionizing how we build AI applications. 

Before MCP, if you wanted an LLM to access live data, you had to write brittle, proprietary plugins. Now, MCP provides a standardized bridge. To explore this, I built **finance-mcp**—a server that exposes real-time stock data and technical indicators directly to Claude Desktop.

Instead of writing complex prompt chains, I simply defined strict Pydantic schemas for tools like `compare_stocks` or `get_history`. Claude natively understands these capabilities and autonomously orchestrates the data retrieval. 

The bottleneck in agentic AI is no longer the model's reasoning—it's the quality of the tools we provide. When you feed an LLM clean, well-structured data via a robust protocol, the results are incredible.

I open-sourced the full implementation (with async TTL caching and fallback patterns). Take a look at how MCP is changing the game:

🔗 https://github.com/yurykudrovsky/finance-mcp

#ArtificialIntelligence #MCP #Claude #SoftwareArchitecture #Agents
