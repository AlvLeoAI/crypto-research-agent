#!/usr/bin/env python3
"""
Technical indicator calculations for crypto price analysis.

Usage:
    python calculate_indicators.py --token BTC --days 14
    
Outputs JSON with RSI, moving averages, and volume analysis.
"""

import argparse
import json
import sys
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class IndicatorResult:
    """Results from technical indicator calculations."""
    token: str
    rsi_14: Optional[float]
    rsi_interpretation: str
    sma_20: Optional[float]
    sma_50: Optional[float]
    trend: str
    volume_vs_average: Optional[float]
    volume_interpretation: str
    data_quality: str
    error: Optional[str] = None


def calculate_rsi(prices: list[float], period: int = 14) -> Optional[float]:
    """
    Calculate RSI (Relative Strength Index).
    
    Args:
        prices: List of closing prices (oldest to newest)
        period: RSI period (default 14)
    
    Returns:
        RSI value between 0-100, or None if insufficient data
    """
    if len(prices) < period + 1:
        return None
    
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    # Initial averages
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    # Smoothed averages for remaining periods
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return round(rsi, 2)


def interpret_rsi(rsi: Optional[float]) -> str:
    """Interpret RSI value."""
    if rsi is None:
        return "Insufficient data"
    
    if rsi >= 80:
        return "Extremely overbought - high reversal risk"
    elif rsi >= 70:
        return "Overbought - potential pullback"
    elif rsi >= 60:
        return "Bullish momentum"
    elif rsi >= 40:
        return "Neutral"
    elif rsi >= 30:
        return "Bearish momentum"
    elif rsi >= 20:
        return "Oversold - potential bounce"
    else:
        return "Extremely oversold - high reversal potential"


def calculate_sma(prices: list[float], period: int) -> Optional[float]:
    """
    Calculate Simple Moving Average.
    
    Args:
        prices: List of closing prices (oldest to newest)
        period: SMA period
    
    Returns:
        SMA value or None if insufficient data
    """
    if len(prices) < period:
        return None
    
    return round(sum(prices[-period:]) / period, 6)


def determine_trend(price: float, sma_20: Optional[float], sma_50: Optional[float], rsi: Optional[float]) -> str:
    """Determine overall trend based on indicators."""
    
    if sma_20 is None:
        return "Insufficient data for trend analysis"
    
    signals = []
    
    # Price vs SMA20
    if price > sma_20:
        signals.append("bullish")
    else:
        signals.append("bearish")
    
    # SMA20 vs SMA50 (if available)
    if sma_50 is not None:
        if sma_20 > sma_50:
            signals.append("bullish")
        else:
            signals.append("bearish")
    
    # RSI confirmation
    if rsi is not None:
        if rsi > 50:
            signals.append("bullish")
        else:
            signals.append("bearish")
    
    bullish_count = signals.count("bullish")
    total = len(signals)
    
    if bullish_count == total:
        return "Strong uptrend"
    elif bullish_count >= total * 0.66:
        return "Moderate uptrend"
    elif bullish_count >= total * 0.33:
        return "Sideways / Choppy"
    elif bullish_count > 0:
        return "Moderate downtrend"
    else:
        return "Strong downtrend"


def analyze_volume(volumes: list[float]) -> tuple[Optional[float], str]:
    """
    Analyze volume relative to recent average.
    
    Args:
        volumes: List of daily volumes (oldest to newest)
    
    Returns:
        Tuple of (ratio vs 7-day avg, interpretation)
    """
    if len(volumes) < 7:
        return None, "Insufficient data"
    
    current = volumes[-1]
    avg_7d = sum(volumes[-8:-1]) / 7  # Previous 7 days, not including current
    
    if avg_7d == 0:
        return None, "No historical volume"
    
    ratio = round(current / avg_7d, 2)
    
    if ratio >= 1.5:
        interpretation = "Significantly elevated - strong market interest"
    elif ratio >= 1.0:
        interpretation = "Above average - moderate interest"
    elif ratio >= 0.75:
        interpretation = "Normal range"
    elif ratio >= 0.5:
        interpretation = "Below average - declining interest"
    else:
        interpretation = "Very low - potential breakout setup or disinterest"
    
    return ratio, interpretation


def calculate_indicators(
    token: str,
    prices: list[float],
    volumes: list[float]
) -> IndicatorResult:
    """
    Calculate all technical indicators for a token.
    
    Args:
        token: Token symbol
        prices: Historical prices (oldest to newest)
        volumes: Historical volumes (oldest to newest)
    
    Returns:
        IndicatorResult with all calculated values
    """
    if not prices:
        return IndicatorResult(
            token=token,
            rsi_14=None,
            rsi_interpretation="No data",
            sma_20=None,
            sma_50=None,
            trend="Unknown",
            volume_vs_average=None,
            volume_interpretation="No data",
            data_quality="No data available",
            error="No price data provided"
        )
    
    current_price = prices[-1]
    
    # Calculate indicators
    rsi = calculate_rsi(prices, 14)
    sma_20 = calculate_sma(prices, 20)
    sma_50 = calculate_sma(prices, 50)
    volume_ratio, volume_interp = analyze_volume(volumes) if volumes else (None, "No volume data")
    
    # Determine data quality
    if len(prices) >= 50:
        data_quality = "Full data - high confidence"
    elif len(prices) >= 20:
        data_quality = "Partial data - moderate confidence"
    elif len(prices) >= 14:
        data_quality = "Limited data - low confidence"
    else:
        data_quality = "Minimal data - very low confidence"
    
    return IndicatorResult(
        token=token,
        rsi_14=rsi,
        rsi_interpretation=interpret_rsi(rsi),
        sma_20=sma_20,
        sma_50=sma_50,
        trend=determine_trend(current_price, sma_20, sma_50, rsi),
        volume_vs_average=volume_ratio,
        volume_interpretation=volume_interp,
        data_quality=data_quality
    )


def main():
    parser = argparse.ArgumentParser(description="Calculate crypto technical indicators")
    parser.add_argument("--token", required=True, help="Token symbol (e.g., BTC)")
    parser.add_argument("--days", type=int, default=14, help="Days of history to analyze")
    parser.add_argument("--prices", help="Comma-separated price history (oldest to newest)")
    parser.add_argument("--volumes", help="Comma-separated volume history (oldest to newest)")
    
    args = parser.parse_args()
    
    # Parse price and volume data
    prices = []
    volumes = []
    
    if args.prices:
        try:
            prices = [float(p.strip()) for p in args.prices.split(",")]
        except ValueError as e:
            print(json.dumps({"error": f"Invalid price data: {e}"}))
            sys.exit(1)
    
    if args.volumes:
        try:
            volumes = [float(v.strip()) for v in args.volumes.split(",")]
        except ValueError as e:
            print(json.dumps({"error": f"Invalid volume data: {e}"}))
            sys.exit(1)
    
    # Calculate indicators
    result = calculate_indicators(args.token, prices, volumes)
    
    # Output as JSON
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()