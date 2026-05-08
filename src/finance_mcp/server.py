import asyncio
import typing
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from pydantic import BaseModel, Field

from finance_mcp.tools.quote import get_quote
from finance_mcp.tools.history import get_history
from finance_mcp.tools.fundamentals import get_fundamentals
from finance_mcp.tools.compare import compare_stocks
from finance_mcp.tools.indicators import calc_indicators

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)
logger = logging.getLogger("finance-mcp")

# Initialize server
server = Server("finance-mcp")


# --- Tool Schemas ---
class SymbolInput(BaseModel):
    symbol: str = Field(description="The stock ticker symbol (e.g. AAPL)")


class HistoryInput(BaseModel):
    symbol: str = Field(description="The stock ticker symbol")
    period: str = Field(
        description="Period to fetch (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"
    )
    interval: str = Field(description="Interval (e.g. 1m, 5m, 1h, 1d, 1wk, 1mo)")


class CompareInput(BaseModel):
    symbols: list[str] = Field(description="List of stock symbols to compare")


class IndicatorsInput(BaseModel):
    symbol: str = Field(description="The stock ticker symbol")
    indicator: str = Field(
        description="Indicator to calculate (SMA20, SMA50, SMA200, RSI, MACD)"
    )


@server.list_tools()  # type: ignore
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="get_quote",
            description="Get current price, change %, and volume for a given stock symbol.",
            inputSchema=SymbolInput.model_json_schema(),
        ),
        types.Tool(
            name="get_history",
            description="Get historical OHLCV data for a given stock symbol.",
            inputSchema=HistoryInput.model_json_schema(),
        ),
        types.Tool(
            name="get_fundamentals",
            description="Get fundamental data (P/E, market cap, yield, sector).",
            inputSchema=SymbolInput.model_json_schema(),
        ),
        types.Tool(
            name="compare_stocks",
            description="Compare multiple stock symbols and return side-by-side metrics.",
            inputSchema=CompareInput.model_json_schema(),
        ),
        types.Tool(
            name="calc_indicators",
            description="Calculate technical indicators (RSI, MACD, SMA20/50/200).",
            inputSchema=IndicatorsInput.model_json_schema(),
        ),
    ]


@server.call_tool()  # type: ignore
async def call_tool(
    name: str, arguments: dict[str, typing.Any]
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Execute a tool call."""
    try:
        if name == "get_quote":
            quote = await get_quote(arguments["symbol"])
            return [
                types.TextContent(type="text", text=quote.model_dump_json(indent=2))
            ]

        elif name == "get_history":
            hist = await get_history(
                arguments["symbol"], arguments["period"], arguments["interval"]
            )
            return [types.TextContent(type="text", text=hist.model_dump_json(indent=2))]

        elif name == "get_fundamentals":
            funds = await get_fundamentals(arguments["symbol"])
            return [
                types.TextContent(type="text", text=funds.model_dump_json(indent=2))
            ]

        elif name == "compare_stocks":
            comp = await compare_stocks(arguments["symbols"])
            return [types.TextContent(type="text", text=comp.model_dump_json(indent=2))]

        elif name == "calc_indicators":
            ind = await calc_indicators(arguments["symbol"], arguments["indicator"])
            return [types.TextContent(type="text", text=ind.model_dump_json(indent=2))]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.error(f"Error calling {name} with args {arguments}: {e}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def run() -> None:
    """Run the MCP server via stdio."""
    logger.info("Starting finance-mcp server")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(run())
