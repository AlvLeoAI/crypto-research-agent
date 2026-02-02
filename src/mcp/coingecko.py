"""
CoinGecko MCP Server Wrapper

Provides access to cryptocurrency price data via CoinGecko API.

This module would wrap a CoinGecko MCP server to provide:
- Current price data
- Historical prices
- Market cap and volume
- Token metadata

For now, this is a placeholder. The actual implementation would either:
1. Use an existing CoinGecko MCP server
2. Implement a simple HTTP client wrapper
"""

import os
from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class TokenPrice:
    """Current price data for a token."""
    symbol: str
    name: str
    price_usd: float
    price_change_24h: float
    price_change_7d: float
    market_cap: float
    volume_24h: float
    last_updated: str


@dataclass
class HistoricalPrice:
    """Historical price point."""
    timestamp: str
    price: float
    volume: float


class CoinGeckoClient:
    """
    Simple CoinGecko API client.
    
    In a full implementation, this would be an MCP server.
    For the portfolio project, this demonstrates the integration pattern.
    """
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COINGECKO_API_KEY")
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers=self._build_headers(),
            timeout=30.0,
        )
    
    def _build_headers(self) -> dict:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["x-cg-demo-api-key"] = self.api_key
        return headers
    
    async def get_price(self, token_id: str) -> Optional[TokenPrice]:
        """
        Get current price for a token.
        
        Args:
            token_id: CoinGecko token ID (e.g., "bitcoin", "ethereum")
        
        Returns:
            TokenPrice object or None if not found
        """
        try:
            response = await self.client.get(
                "/coins/markets",
                params={
                    "vs_currency": "usd",
                    "ids": token_id,
                    "order": "market_cap_desc",
                    "per_page": 1,
                    "page": 1,
                    "sparkline": False,
                    "price_change_percentage": "24h,7d",
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None
            
            coin = data[0]
            return TokenPrice(
                symbol=coin["symbol"].upper(),
                name=coin["name"],
                price_usd=coin["current_price"],
                price_change_24h=coin.get("price_change_percentage_24h", 0),
                price_change_7d=coin.get("price_change_percentage_7d_in_currency", 0),
                market_cap=coin.get("market_cap", 0),
                volume_24h=coin.get("total_volume", 0),
                last_updated=coin.get("last_updated", ""),
            )
        except Exception as e:
            print(f"Error fetching price for {token_id}: {e}")
            return None
    
    async def get_historical_prices(
        self, 
        token_id: str, 
        days: int = 14
    ) -> list[HistoricalPrice]:
        """
        Get historical prices for indicator calculations.
        
        Args:
            token_id: CoinGecko token ID
            days: Number of days of history
        
        Returns:
            List of HistoricalPrice objects
        """
        try:
            response = await self.client.get(
                f"/coins/{token_id}/market_chart",
                params={
                    "vs_currency": "usd",
                    "days": days,
                }
            )
            response.raise_for_status()
            data = response.json()
            
            prices = []
            for price_point, volume_point in zip(data["prices"], data["total_volumes"]):
                prices.append(HistoricalPrice(
                    timestamp=str(price_point[0]),
                    price=price_point[1],
                    volume=volume_point[1],
                ))
            
            return prices
        except Exception as e:
            print(f"Error fetching historical prices for {token_id}: {e}")
            return []
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Token ID mapping (common symbols to CoinGecko IDs)
TOKEN_ID_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "ADA": "cardano",
    "DOT": "polkadot",
    "AVAX": "avalanche-2",
    "MATIC": "matic-network",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "ATOM": "cosmos",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "SHIB": "shiba-inu",
    "LTC": "litecoin",
    "BCH": "bitcoin-cash",
}


def get_token_id(symbol_or_name: str) -> str:
    """
    Convert a symbol or name to CoinGecko token ID.
    
    Args:
        symbol_or_name: Token symbol (BTC) or name (bitcoin)
    
    Returns:
        CoinGecko token ID
    """
    upper = symbol_or_name.upper()
    if upper in TOKEN_ID_MAP:
        return TOKEN_ID_MAP[upper]
    
    # Assume it's already a token ID if not in map
    return symbol_or_name.lower()