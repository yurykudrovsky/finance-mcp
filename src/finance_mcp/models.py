from pydantic import BaseModel, Field
from typing import List, Optional


class Quote(BaseModel):
    symbol: str = Field(description="The stock ticker symbol")
    price: float = Field(description="Current stock price")
    change_percent: float = Field(description="Percentage change in price")
    volume: int = Field(description="Trading volume")


class OHLCV(BaseModel):
    date: str = Field(description="Date/time of the data point")
    open: float = Field(description="Open price")
    high: float = Field(description="High price")
    low: float = Field(description="Low price")
    close: float = Field(description="Close price")
    volume: int = Field(description="Trading volume")


class History(BaseModel):
    symbol: str = Field(description="The stock ticker symbol")
    data: List[OHLCV] = Field(description="List of OHLCV data points")


class Fundamentals(BaseModel):
    symbol: str = Field(description="The stock ticker symbol")
    pe_ratio: Optional[float] = Field(
        description="Price to Earnings ratio", default=None
    )
    market_cap: Optional[int] = Field(description="Market capitalization", default=None)
    dividend_yield: Optional[float] = Field(
        description="Dividend yield percentage", default=None
    )
    sector: Optional[str] = Field(description="Company sector", default=None)


class Metrics(BaseModel):
    price: Optional[float] = None
    pe_ratio: Optional[float] = None
    market_cap: Optional[int] = None
    change_percent: Optional[float] = None


class Comparison(BaseModel):
    symbols: List[str] = Field(description="List of compared symbols")
    metrics: dict[str, Metrics] = Field(description="Metrics keyed by symbol")


class IndicatorData(BaseModel):
    date: str
    value: float


class Indicators(BaseModel):
    symbol: str = Field(description="The stock ticker symbol")
    indicator: str = Field(description="Name of the indicator (e.g. RSI, MACD, SMA)")
    data: List[IndicatorData] = Field(description="Indicator values over time")
