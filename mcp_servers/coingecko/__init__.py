"""
CoinGecko MCP Server

Provides cryptocurrency price data, historical prices, market overview,
and token search functionality via the Model Context Protocol.
"""

from mcp_servers.coingecko.server import CoinGeckoMCPHandler, MCPServer
from mcp_servers.coingecko.client import CoinGeckoClient, TokenPrice, HistoricalDataPoint, MarketOverview
from mcp_servers.coingecko.tools import TOOLS, format_tools_for_claude

__all__ = [
    "CoinGeckoMCPHandler",
    "MCPServer",
    "CoinGeckoClient",
    "TokenPrice",
    "HistoricalDataPoint",
    "MarketOverview",
    "TOOLS",
    "format_tools_for_claude",
]