#!/usr/bin/env python3
"""
CoinGecko MCP Server

A Model Context Protocol server that provides cryptocurrency data tools.
Can be run as a standalone server or used directly by the agent.

Usage:
    # As standalone server (for MCP clients)
    python -m mcp_servers.coingecko.server
    
    # Or use the handler directly in Python
    from mcp_servers.coingecko.server import CoinGeckoMCPHandler
    handler = CoinGeckoMCPHandler()
    result = await handler.handle_tool_call("get_crypto_price", {"token": "BTC"})
"""

import asyncio
import json
import sys
from typing import Any, Optional
from dataclasses import asdict

from mcp_servers.coingecko.client import CoinGeckoClient, TokenPrice, HistoricalDataPoint, MarketOverview
from mcp_servers.coingecko.tools import TOOLS, get_tool_by_name


class CoinGeckoMCPHandler:
    """
    MCP request handler for CoinGecko tools.
    
    This can be used:
    1. Directly by importing and calling handle_tool_call()
    2. As part of a full MCP server over stdio
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the handler.
        
        Args:
            api_key: CoinGecko API key (optional, uses free tier if not provided)
        """
        self.api_key = api_key
        self._client: Optional[CoinGeckoClient] = None
    
    @property
    def client(self) -> CoinGeckoClient:
        """Lazy initialization of the client."""
        if self._client is None:
            self._client = CoinGeckoClient(self.api_key)
        return self._client
    
    async def close(self):
        """Close the client connection."""
        if self._client is not None:
            await self._client.close()
            self._client = None
    
    def list_tools(self) -> list[dict]:
        """Return list of available tools."""
        return TOOLS
    
    async def handle_tool_call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Handle a tool call request.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool result as a dictionary
        """
        try:
            if tool_name == "get_crypto_price":
                return await self._get_crypto_price(arguments)
            elif tool_name == "get_historical_prices":
                return await self._get_historical_prices(arguments)
            elif tool_name == "get_market_overview":
                return await self._get_market_overview(arguments)
            elif tool_name == "search_tokens":
                return await self._search_tokens(arguments)
            elif tool_name == "get_trending_tokens":
                return await self._get_trending_tokens(arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def _get_crypto_price(self, args: dict) -> dict:
        """Handle get_crypto_price tool call."""
        token = args.get("token")
        if not token:
            return {"error": "Missing required argument: token"}
        
        result = await self.client.get_price(token)
        
        if result is None:
            return {
                "error": f"Token not found: {token}",
                "suggestion": "Try using search_tokens to find the correct token ID"
            }
        
        return {
            "success": True,
            "data": result.to_dict()
        }
    
    async def _get_historical_prices(self, args: dict) -> dict:
        """Handle get_historical_prices tool call."""
        token = args.get("token")
        if not token:
            return {"error": "Missing required argument: token"}
        
        days = args.get("days", 14)
        
        result = await self.client.get_historical_data(token, days)
        
        if not result:
            return {
                "error": f"Could not fetch historical data for: {token}",
                "suggestion": "Token may not exist or API rate limit reached"
            }
        
        # Return summary + sampled data points (full data can be very large)
        prices = [p.price_usd for p in result]
        
        return {
            "success": True,
            "data": {
                "token": token,
                "days": days,
                "data_points": len(result),
                "price_start": prices[0] if prices else None,
                "price_end": prices[-1] if prices else None,
                "price_high": max(prices) if prices else None,
                "price_low": min(prices) if prices else None,
                "price_change_percent": ((prices[-1] - prices[0]) / prices[0] * 100) if prices and prices[0] else None,
                # Include sampled points for charting (every nth point)
                "sampled_points": [
                    {
                        "datetime": p.datetime_utc,
                        "price": p.price_usd,
                        "volume": p.volume_usd
                    }
                    for i, p in enumerate(result) if i % max(1, len(result) // 20) == 0
                ],
                # Include raw prices for indicator calculations
                "prices": prices,
                "volumes": [p.volume_usd for p in result]
            }
        }
    
    async def _get_market_overview(self, args: dict) -> dict:
        """Handle get_market_overview tool call."""
        result = await self.client.get_market_overview()
        
        if result is None:
            return {"error": "Could not fetch market overview"}
        
        return {
            "success": True,
            "data": {
                "total_market_cap_usd": result.total_market_cap_usd,
                "total_market_cap_formatted": f"${result.total_market_cap_usd / 1e12:.2f}T",
                "total_volume_24h_usd": result.total_volume_24h_usd,
                "total_volume_formatted": f"${result.total_volume_24h_usd / 1e9:.1f}B",
                "btc_dominance_percent": round(result.btc_dominance_percent, 2),
                "eth_dominance_percent": round(result.eth_dominance_percent, 2),
                "active_cryptocurrencies": result.active_cryptocurrencies,
                "markets": result.markets,
                "market_cap_change_24h_percent": round(result.market_cap_change_24h_percent, 2),
                "last_updated": result.last_updated
            }
        }
    
    async def _search_tokens(self, args: dict) -> dict:
        """Handle search_tokens tool call."""
        query = args.get("query")
        if not query:
            return {"error": "Missing required argument: query"}
        
        limit = args.get("limit", 10)
        
        result = await self.client.search_tokens(query, limit)
        
        return {
            "success": True,
            "query": query,
            "results": result,
            "count": len(result)
        }
    
    async def _get_trending_tokens(self, args: dict) -> dict:
        """Handle get_trending_tokens tool call."""
        result = await self.client.get_trending()
        
        return {
            "success": True,
            "trending": result,
            "count": len(result)
        }


class MCPServer:
    """
    Full MCP server that communicates over stdio.
    
    Implements the Model Context Protocol for external MCP clients.
    """
    
    def __init__(self, handler: CoinGeckoMCPHandler):
        self.handler = handler
    
    async def handle_request(self, request: dict) -> dict:
        """Handle an incoming MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "coingecko-mcp",
                        "version": "0.1.0"
                    },
                    "capabilities": {
                        "tools": {}
                    }
                }
            elif method == "tools/list":
                result = {
                    "tools": self.handler.list_tools()
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                tool_result = await self.handler.handle_tool_call(tool_name, arguments)
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(tool_result, indent=2)
                        }
                    ]
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
    
    async def run_stdio(self):
        """Run the server over stdio."""
        print("CoinGecko MCP Server started", file=sys.stderr)
        
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                
                try:
                    request = json.loads(line)
                    response = await self.handle_request(request)
                    print(json.dumps(response), flush=True)
                except json.JSONDecodeError:
                    print(json.dumps({
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }), flush=True)
        finally:
            await self.handler.close()


async def main():
    """Main entry point for running as standalone server."""
    handler = CoinGeckoMCPHandler()
    server = MCPServer(handler)
    await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main())