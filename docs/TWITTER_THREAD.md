# Twitter / X Thread

**Tweet 1:**
I built an open-source tool that turns Claude Desktop into a live quantitative financial analyst. 📈🤖

Meet **finance-mcp**: A fast, asynchronous Model Context Protocol (MCP) server that pipes real-time stock data straight to the LLM. 

Zero API keys required.
👇 Demo & Details:
[Embed demo.gif here]

**Tweet 2:**
Why build this? Because giving LLMs raw access to undocumented endpoints usually ends in brittle, hallucinating agents. 

I wanted to see what happens when you feed Claude clean, strictly-typed financial data using the new MCP standard. The results are magical. ✨

**Tweet 3:**
To make it production-grade, I implemented a robust `DataProvider` fallback pattern. 

The primary engine is `yfinance` (because it’s frictionless). But if it hits an exception or rate-limit, the server seamlessly degrades to Alpha Vantage without dropping the agent's context.

**Tweet 4:**
LLMs are chatty—they often query the same ticker multiple times to double-check their reasoning. 

To prevent instant upstream throttling, I engineered a lightweight, async TTL cache directly into the tool layer. Fast-moving quotes get 60s, slow fundamentals get 1h. ⏱️

**Tweet 5:**
The biggest lesson? The bottleneck in agentic AI isn't reasoning anymore—it's tool quality. 

When you give an LLM messy data, it fails. When you give it perfectly structured Pydantic JSON via MCP, it orchestrates complex workflows effortlessly. 🧩

**Tweet 6:**
Want to give your AI agent access to live quotes, OHLCV history, and technical indicators? 

The code is fully open-source, async from the ground up, and thoroughly tested. 

Star the repo and try it out here:
🔗 https://github.com/yurykudrovsky/finance-mcp
