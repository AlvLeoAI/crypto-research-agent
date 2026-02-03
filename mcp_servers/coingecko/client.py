"""
CoinGecko API Client

Low-level client for interacting with the CoinGecko API.
Used by the MCP server to fetch cryptocurrency data.
"""

import os
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

import httpx


@dataclass
class TokenPrice:
    """Current price data for a token."""
    id: str
    symbol: str
    name: str
    current_price_usd: float
    price_change_24h_percent: float
    price_change_7d_percent: float
    market_cap_usd: float
    total_volume_24h_usd: float
    circulating_supply: float
    total_supply: Optional[float]
    ath_usd: float
    ath_change_percent: float
    atl_usd: float
    last_updated: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class HistoricalDataPoint:
    """Single historical data point."""
    timestamp: int
    datetime_utc: str
    price_usd: float
    market_cap_usd: float
    volume_usd: float


@dataclass
class MarketOverview:
    """Overall crypto market data."""
    total_market_cap_usd: float
    total_volume_24h_usd: float
    btc_dominance_percent: float
    eth_dominance_percent: float
    active_cryptocurrencies: int
    markets: int
    market_cap_change_24h_percent: float
    last_updated: str


class CoinGeckoClient:
    """
    Async client for CoinGecko API.

    Supports both free and Pro API tiers.
    """

    FREE_BASE_URL = "https://api.coingecko.com/api/v3"
    PRO_BASE_URL = "https://pro-api.coingecko.com/api/v3"

    # Common token symbol to CoinGecko ID mapping
    SYMBOL_TO_ID = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "ADA": "cardano",
        "DOT": "polkadot",
        "AVAX": "avalanche-2",
        "MATIC": "matic-network",
        "POL": "matic-network",
        "LINK": "chainlink",
        "UNI": "uniswap",
        "ATOM": "cosmos",
        "XRP": "ripple",
        "DOGE": "dogecoin",
        "SHIB": "shiba-inu",
        "LTC": "litecoin",
        "BCH": "bitcoin-cash",
        "NEAR": "near",
        "APT": "aptos",
        "ARB": "arbitrum",
        "OP": "optimism",
        "SUI": "sui",
        "SEI": "sei-network",
        "TIA": "celestia",
        "INJ": "injective-protocol",
        "FET": "fetch-ai",
        "RNDR": "render-token",
        "GRT": "the-graph",
        "FIL": "filecoin",
        "AAVE": "aave",
        "MKR": "maker",
        "CRV": "curve-dao-token",
        "LDO": "lido-dao",
        "RPL": "rocket-pool",
        "SNX": "synthetix-network-token",
        "COMP": "compound-governance-token",
        "PEPE": "pepe",
        "WIF": "dogwifcoin",
        "BONK": "bonk",
        "FLOKI": "floki",
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the client.

        Args:
            api_key: CoinGecko Pro API key (optional, uses free tier if not provided)
        """
        self.api_key = api_key or os.getenv("COINGECKO_API_KEY")
        self.is_pro = bool(self.api_key)
        self.base_url = self.PRO_BASE_URL if self.is_pro else self.FREE_BASE_URL

        headers = {"Accept": "application/json"}
        if self.is_pro:
            headers["x-cg-pro-api-key"] = self.api_key

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=30.0,
        )

    def resolve_token_id(self, symbol_or_id: str) -> str:
        """
        Resolve a symbol or name to CoinGecko token ID.

        Args:
            symbol_or_id: Token symbol (BTC), name (bitcoin), or ID

        Returns:
            CoinGecko token ID
        """
        upper = symbol_or_id.upper().strip()
        if upper in self.SYMBOL_TO_ID:
            return self.SYMBOL_TO_ID[upper]
        return symbol_or_id.lower().strip()

    async def get_price(self, token: str) -> Optional[TokenPrice]:
        """
        Get current price and market data for a token.

        Args:
            token: Token symbol (BTC) or CoinGecko ID (bitcoin)

        Returns:
            TokenPrice object or None if not found
        """
        token_id = self.resolve_token_id(token)

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
                id=coin["id"],
                symbol=coin["symbol"].upper(),
                name=coin["name"],
                current_price_usd=coin.get("current_price", 0),
                price_change_24h_percent=coin.get("price_change_percentage_24h", 0) or 0,
                price_change_7d_percent=coin.get("price_change_percentage_7d_in_currency", 0) or 0,
                market_cap_usd=coin.get("market_cap", 0) or 0,
                total_volume_24h_usd=coin.get("total_volume", 0) or 0,
                circulating_supply=coin.get("circulating_supply", 0) or 0,
                total_supply=coin.get("total_supply"),
                ath_usd=coin.get("ath", 0) or 0,
                ath_change_percent=coin.get("ath_change_percentage", 0) or 0,
                atl_usd=coin.get("atl", 0) or 0,
                last_updated=coin.get("last_updated", datetime.utcnow().isoformat()),
            )

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            print(f"Error fetching price for {token}: {e}")
            return None

    async def get_historical_data(
        self,
        token: str,
        days: int = 14
    ) -> list[HistoricalDataPoint]:
        """
        Get historical price data for technical analysis.

        Args:
            token: Token symbol or ID
            days: Number of days of history (1, 7, 14, 30, 90, 180, 365, max)

        Returns:
            List of HistoricalDataPoint objects
        """
        token_id = self.resolve_token_id(token)

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

            points = []
            prices = data.get("prices", [])
            market_caps = data.get("market_caps", [])
            volumes = data.get("total_volumes", [])

            for i, (timestamp, price) in enumerate(prices):
                market_cap = market_caps[i][1] if i < len(market_caps) else 0
                volume = volumes[i][1] if i < len(volumes) else 0

                dt = datetime.utcfromtimestamp(timestamp / 1000)

                points.append(HistoricalDataPoint(
                    timestamp=timestamp,
                    datetime_utc=dt.isoformat() + "Z",
                    price_usd=price,
                    market_cap_usd=market_cap,
                    volume_usd=volume,
                ))

            return points

        except Exception as e:
            print(f"Error fetching historical data for {token}: {e}")
            return []

    async def get_market_overview(self) -> Optional[MarketOverview]:
        """
        Get overall crypto market statistics.

        Returns:
            MarketOverview object
        """
        try:
            response = await self.client.get("/global")
            response.raise_for_status()
            data = response.json()["data"]

            return MarketOverview(
                total_market_cap_usd=data.get("total_market_cap", {}).get("usd", 0),
                total_volume_24h_usd=data.get("total_volume", {}).get("usd", 0),
                btc_dominance_percent=data.get("market_cap_percentage", {}).get("btc", 0),
                eth_dominance_percent=data.get("market_cap_percentage", {}).get("eth", 0),
                active_cryptocurrencies=data.get("active_cryptocurrencies", 0),
                markets=data.get("markets", 0),
                market_cap_change_24h_percent=data.get("market_cap_change_percentage_24h_usd", 0),
                last_updated=datetime.utcfromtimestamp(data.get("updated_at", 0)).isoformat() + "Z",
            )

        except Exception as e:
            print(f"Error fetching market overview: {e}")
            return None

    async def search_tokens(self, query: str, limit: int = 10) -> list[dict]:
        """
        Search for tokens by name or symbol.

        Args:
            query: Search query
            limit: Max results to return

        Returns:
            List of matching tokens with id, symbol, name, market_cap_rank
        """
        try:
            response = await self.client.get(
                "/search",
                params={"query": query}
            )
            response.raise_for_status()
            data = response.json()

            coins = data.get("coins", [])[:limit]
            return [
                {
                    "id": coin["id"],
                    "symbol": coin["symbol"].upper(),
                    "name": coin["name"],
                    "market_cap_rank": coin.get("market_cap_rank"),
                }
                for coin in coins
            ]

        except Exception as e:
            print(f"Error searching for {query}: {e}")
            return []

    async def get_trending(self) -> list[dict]:
        """
        Get trending tokens (top 7 by search popularity).

        Returns:
            List of trending tokens
        """
        try:
            response = await self.client.get("/search/trending")
            response.raise_for_status()
            data = response.json()

            return [
                {
                    "id": coin["item"]["id"],
                    "symbol": coin["item"]["symbol"].upper(),
                    "name": coin["item"]["name"],
                    "market_cap_rank": coin["item"].get("market_cap_rank"),
                    "score": coin["item"].get("score"),
                }
                for coin in data.get("coins", [])
            ]

        except Exception as e:
            print(f"Error fetching trending: {e}")
            return []

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
