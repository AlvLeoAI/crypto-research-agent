"""
Price Analyst Subagent

Specialized agent for technical analysis, price data, and market indicators.
Uses CoinGecko MCP tools to fetch real market data.
"""

import json
from pathlib import Path
from anthropic import Anthropic

from src.utils.prompts import load_prompt
from mcp_servers.coingecko import CoinGeckoMCPHandler


def load_skill_content() -> tuple[str, str]:
    """Load the technical-analysis skill and references."""
    skill_path = Path(".claude/skills/technical-analysis/SKILL.md")
    indicators_path = Path(".claude/skills/technical-analysis/references/indicators.md")
    
    skill = skill_path.read_text() if skill_path.exists() else ""
    indicators = indicators_path.read_text() if indicators_path.exists() else ""
    
    return skill, indicators


def calculate_rsi(prices: list[float], period: int = 14) -> float | None:
    """Calculate RSI from price list."""
    if len(prices) < period + 1:
        return None
    
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def calculate_sma(prices: list[float], period: int) -> float | None:
    """Calculate Simple Moving Average."""
    if len(prices) < period:
        return None
    return round(sum(prices[-period:]) / period, 2)


async def run_price_analyst(token: str, client: Anthropic, model: str) -> str:
    """
    Run the price analyst subagent with real MCP data.
    
    Args:
        token: Cryptocurrency token to analyze (e.g., "bitcoin", "ETH")
        client: Anthropic client instance
        model: Model to use for analysis
    
    Returns:
        Price analysis report as markdown string
    """
    # Load prompt and skill
    try:
        agent_prompt = load_prompt("price_analyst")
    except FileNotFoundError:
        agent_prompt = "You are a cryptocurrency price analyst."
    
    skill_content, indicators_ref = load_skill_content()
    
    # Initialize MCP handler and fetch real data
    mcp_handler = CoinGeckoMCPHandler()
    
    try:
        # Fetch current price
        price_result = await mcp_handler.handle_tool_call(
            "get_crypto_price", 
            {"token": token}
        )
        
        # Fetch historical data for indicators
        historical_result = await mcp_handler.handle_tool_call(
            "get_historical_prices",
            {"token": token, "days": 14}
        )
        
        # Fetch market overview for context
        market_result = await mcp_handler.handle_tool_call(
            "get_market_overview",
            {}
        )
        
    finally:
        await mcp_handler.close()
    
    # Process the data
    price_data = price_result.get("data", {}) if price_result.get("success") else {}
    historical_data = historical_result.get("data", {}) if historical_result.get("success") else {}
    market_data = market_result.get("data", {}) if market_result.get("success") else {}
    
    # Calculate technical indicators from historical data
    prices = historical_data.get("prices", [])
    volumes = historical_data.get("volumes", [])
    
    rsi = calculate_rsi(prices) if prices else None
    sma_20 = calculate_sma(prices, 20) if len(prices) >= 20 else None
    sma_50 = calculate_sma(prices, 50) if len(prices) >= 50 else None
    
    # Calculate volume trend
    volume_avg = sum(volumes[-7:]) / 7 if len(volumes) >= 7 else None
    current_volume = volumes[-1] if volumes else None
    volume_ratio = round(current_volume / volume_avg, 2) if volume_avg and current_volume else None
    
    # Determine trend
    current_price = price_data.get("current_price_usd", 0)
    if sma_20 and sma_50:
        if current_price > sma_20 > sma_50:
            trend = "Strong Uptrend"
        elif current_price > sma_20:
            trend = "Uptrend"
        elif current_price < sma_20 < sma_50:
            trend = "Strong Downtrend"
        elif current_price < sma_20:
            trend = "Downtrend"
        else:
            trend = "Sideways"
    elif sma_20:
        trend = "Uptrend" if current_price > sma_20 else "Downtrend"
    else:
        trend = "Insufficient data"
    
    # Interpret RSI
    if rsi is not None:
        if rsi >= 70:
            rsi_interpretation = "Overbought - potential pullback"
        elif rsi >= 60:
            rsi_interpretation = "Bullish momentum"
        elif rsi >= 40:
            rsi_interpretation = "Neutral"
        elif rsi >= 30:
            rsi_interpretation = "Bearish momentum"
        else:
            rsi_interpretation = "Oversold - potential bounce"
    else:
        rsi_interpretation = "Insufficient data"
    
    # Build structured data for Claude to analyze
    analysis_data = {
        "token": {
            "symbol": price_data.get("symbol", token.upper()),
            "name": price_data.get("name", token),
            "current_price": price_data.get("current_price_usd"),
            "price_change_24h": price_data.get("price_change_24h_percent"),
            "price_change_7d": price_data.get("price_change_7d_percent"),
            "market_cap": price_data.get("market_cap_usd"),
            "volume_24h": price_data.get("total_volume_24h_usd"),
            "ath": price_data.get("ath_usd"),
            "ath_change_percent": price_data.get("ath_change_percent"),
        },
        "technical_indicators": {
            "rsi_14": rsi,
            "rsi_interpretation": rsi_interpretation,
            "sma_20": sma_20,
            "sma_50": sma_50,
            "trend": trend,
            "volume_ratio": volume_ratio,
            "volume_interpretation": "Above average" if volume_ratio and volume_ratio > 1 else "Below average" if volume_ratio else "Unknown"
        },
        "historical": {
            "days": 14,
            "price_start": historical_data.get("price_start"),
            "price_end": historical_data.get("price_end"),
            "price_high": historical_data.get("price_high"),
            "price_low": historical_data.get("price_low"),
            "price_change_percent": historical_data.get("price_change_percent"),
        },
        "market_context": {
            "total_market_cap": market_data.get("total_market_cap_formatted"),
            "btc_dominance": market_data.get("btc_dominance_percent"),
            "market_change_24h": market_data.get("market_cap_change_24h_percent"),
        }
    }
    
    # Build the system prompt with skill
    system_prompt = f"""{agent_prompt}

## Skill: technical-analysis

{skill_content}

## Reference: indicators.md

{indicators_ref}
"""
    
    # User request with real data
    user_message = f"""Analyze {token} using the following REAL market data I've fetched:

## Current Price Data
{json.dumps(analysis_data['token'], indent=2)}

## Technical Indicators (calculated from 14-day history)
{json.dumps(analysis_data['technical_indicators'], indent=2)}

## 14-Day Historical Summary
{json.dumps(analysis_data['historical'], indent=2)}

## Market Context
{json.dumps(analysis_data['market_context'], indent=2)}

Based on this real data, provide your technical analysis following the skill's output format.
Include:
1. Current metrics summary
2. Technical indicator interpretation
3. Key support/resistance levels (estimate from the high/low data)
4. Brief technical outlook

This is LIVE DATA - provide specific analysis based on these exact numbers."""
    
    # Call Claude to interpret the data
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    return response.content[0].text