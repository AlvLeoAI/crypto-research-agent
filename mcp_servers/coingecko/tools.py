"""
MCP Tool Definitions for CoinGecko

Defines the tools that Claude can use to interact with CoinGecko data.
"""

from typing import Any

# Tool definitions following MCP schema
TOOLS = [
    {
        "name": "get_crypto_price",
        "description": """Get current price and market data for a cryptocurrency.

Returns: current price (USD), 24h change %, 7d change %, market cap, volume, 
circulating supply, all-time high, and last updated timestamp.

Use this for: Current price checks, market cap comparisons, basic token info.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "Token symbol (e.g., 'BTC', 'ETH') or CoinGecko ID (e.g., 'bitcoin', 'ethereum')"
                }
            },
            "required": ["token"]
        }
    },
    {
        "name": "get_historical_prices",
        "description": """Get historical price data for technical analysis.

Returns: List of data points with timestamp, price, market cap, and volume.
Data granularity depends on the days parameter:
- 1 day: ~5 minute intervals
- 7-14 days: hourly intervals  
- 30+ days: daily intervals

Use this for: Calculating RSI, moving averages, identifying trends, chart analysis.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "Token symbol (e.g., 'BTC') or CoinGecko ID (e.g., 'bitcoin')"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days of historical data (1, 7, 14, 30, 90, 180, 365)",
                    "default": 14
                }
            },
            "required": ["token"]
        }
    },
    {
        "name": "get_market_overview",
        "description": """Get overall cryptocurrency market statistics.

Returns: Total market cap, 24h volume, BTC dominance %, ETH dominance %,
number of active cryptocurrencies, market cap change 24h %.

Use this for: Understanding market conditions, BTC dominance analysis, 
market-wide sentiment context.""",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "search_tokens",
        "description": """Search for cryptocurrency tokens by name or symbol.

Returns: List of matching tokens with ID, symbol, name, and market cap rank.

Use this for: Finding the correct token ID, discovering similar tokens,
handling ambiguous token references.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (token name or symbol)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_trending_tokens",
        "description": """Get currently trending cryptocurrencies.

Returns: Top 7 tokens by search popularity on CoinGecko, with ID, symbol,
name, market cap rank, and trending score.

Use this for: Market sentiment, discovering popular tokens, trend analysis.""",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


def get_tool_by_name(name: str) -> dict | None:
    """Get a tool definition by name."""
    for tool in TOOLS:
        if tool["name"] == name:
            return tool
    return None


def get_all_tool_names() -> list[str]:
    """Get list of all tool names."""
    return [tool["name"] for tool in TOOLS]


def format_tools_for_claude() -> list[dict]:
    """
    Format tools for use with Claude's tool_use feature.
    
    Returns tools in the format expected by anthropic.messages.create()
    """
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["input_schema"]
        }
        for tool in TOOLS
    ]