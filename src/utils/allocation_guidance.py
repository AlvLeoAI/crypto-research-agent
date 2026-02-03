"""
Weekly Allocation Guidance Generator

Deterministic logic to generate allocation guidance from technical signals.
Used in the Notion report output.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AllocationSignals:
    """Input signals for allocation guidance calculation."""
    current_price: Optional[float] = None
    price_change_7d: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    rsi_14: Optional[float] = None
    support_1: Optional[float] = None
    resistance_1: Optional[float] = None
    volume_status: Optional[str] = None  # "below", "avg", "above"
    news_available: bool = True
    sentiment_available: bool = True


@dataclass
class AllocationGuidance:
    """Output allocation guidance."""
    action_bias: str  # Pause, Hold, Light Accumulate, Accumulate
    allocation_hint: str  # 0%, 25%, 50%, 100%
    time_horizon: str = "1 week"
    why_bullets: list[str] = None
    invalidation_triggers: list[str] = None
    next_check_bullets: list[str] = None

    def __post_init__(self):
        if self.why_bullets is None:
            self.why_bullets = []
        if self.invalidation_triggers is None:
            self.invalidation_triggers = []
        if self.next_check_bullets is None:
            self.next_check_bullets = []


def determine_structure(price: Optional[float], sma_20: Optional[float], sma_50: Optional[float]) -> str:
    """
    Determine price structure relative to moving averages.

    Returns:
        "bullish" - price > SMA50 AND price > SMA20
        "warning" - price > SMA50 AND price <= SMA20
        "risk_off" - price <= SMA50
        "unknown" - insufficient data
    """
    if price is None or sma_50 is None:
        return "unknown"

    if price <= sma_50:
        return "risk_off"

    # price > sma_50
    if sma_20 is None:
        return "bullish"  # Default to bullish if only SMA50 available and price above it

    if price > sma_20:
        return "bullish"
    else:
        return "warning"


def determine_rsi_regime(rsi: Optional[float]) -> str:
    """
    Determine RSI momentum regime.

    Returns:
        "low" - RSI < 45
        "neutral" - 45 <= RSI <= 60
        "positive" - RSI > 60
        "unknown" - no RSI data
    """
    if rsi is None:
        return "unknown"

    if rsi < 45:
        return "low"
    elif rsi <= 60:
        return "neutral"
    else:
        return "positive"


def is_key_support_broken(price: Optional[float], support_1: Optional[float], sma_50: Optional[float]) -> bool:
    """
    Check if key support is broken.
    Uses first support level or SMA50 as proxy.
    """
    if price is None:
        return False

    # Check support_1 first
    if support_1 is not None and price < support_1:
        return True

    # Use SMA50 as proxy if no support level
    if support_1 is None and sma_50 is not None and price < sma_50:
        return True

    return False


def calculate_base_bias(
    structure: str,
    rsi_regime: str,
    support_broken: bool
) -> str:
    """
    Calculate base action bias before data limitation adjustment.

    Mapping:
    - bullish + (neutral or positive) + support intact -> Accumulate
    - warning + neutral -> Light Accumulate
    - risk_off + no extreme breakdown -> Hold
    - risk_off + support broken -> Pause
    - unknown structure -> Hold (conservative default)
    """
    if structure == "unknown":
        return "Hold"

    if structure == "bullish":
        if rsi_regime in ("neutral", "positive", "unknown"):
            if not support_broken:
                return "Accumulate"
            else:
                return "Light Accumulate"
        elif rsi_regime == "low":
            return "Light Accumulate"

    elif structure == "warning":
        if rsi_regime == "neutral":
            return "Light Accumulate"
        elif rsi_regime == "low":
            return "Hold"
        else:
            return "Light Accumulate"

    elif structure == "risk_off":
        if support_broken:
            return "Pause"
        else:
            return "Hold"

    return "Hold"


def downgrade_bias(bias: str) -> str:
    """
    Downgrade bias by one step due to data limitations.

    Accumulate -> Light Accumulate
    Light Accumulate -> Hold
    Hold -> Pause
    Pause -> Pause (cannot go lower)
    """
    downgrade_map = {
        "Accumulate": "Light Accumulate",
        "Light Accumulate": "Hold",
        "Hold": "Pause",
        "Pause": "Pause",
    }
    return downgrade_map.get(bias, "Hold")


def bias_to_allocation_hint(bias: str) -> str:
    """
    Map action bias to allocation hint percentage.

    Pause -> 0%
    Hold -> 25%
    Light Accumulate -> 50%
    Accumulate -> 100%
    """
    allocation_map = {
        "Pause": "0%",
        "Hold": "25%",
        "Light Accumulate": "50%",
        "Accumulate": "100%",
    }
    return allocation_map.get(bias, "25%")


def format_price(price: Optional[float]) -> str:
    """Format price for display."""
    if price is None:
        return "N/A"
    if price >= 1000:
        return f"${price:,.0f}"
    elif price >= 1:
        return f"${price:,.2f}"
    else:
        return f"${price:.4f}"


def build_why_bullets(
    signals: AllocationSignals,
    structure: str,
    rsi_regime: str,
    data_limited: bool,
    final_bias: str
) -> list[str]:
    """Build the 'Why' explanation bullets."""
    bullets = []

    # Structure explanation
    if structure == "bullish":
        bullets.append(f"Price above both SMA20 ({format_price(signals.sma_20)}) and SMA50 ({format_price(signals.sma_50)}) — bullish structure intact")
    elif structure == "warning":
        bullets.append(f"Price above SMA50 ({format_price(signals.sma_50)}) but below SMA20 ({format_price(signals.sma_20)}) — warning structure, potential pullback")
    elif structure == "risk_off":
        bullets.append(f"Price below SMA50 ({format_price(signals.sma_50)}) — risk-off structure, trend weakening")
    else:
        bullets.append("Insufficient moving average data for structure determination — defaulting to conservative stance")

    # RSI explanation
    if signals.rsi_14 is not None:
        if rsi_regime == "positive":
            bullets.append(f"RSI at {signals.rsi_14:.1f} shows positive momentum (>60)")
        elif rsi_regime == "neutral":
            bullets.append(f"RSI at {signals.rsi_14:.1f} in neutral zone (45-60) — no extreme")
        elif rsi_regime == "low":
            bullets.append(f"RSI at {signals.rsi_14:.1f} below 45 — momentum weakening")

    # 7d correction context
    if signals.price_change_7d is not None:
        if signals.price_change_7d <= -10:
            bullets.append(f"7-day correction of {signals.price_change_7d:.1f}% creates potential mean-reversion setup")
        elif signals.price_change_7d <= -5:
            bullets.append(f"Modest 7-day pullback ({signals.price_change_7d:.1f}%) — watching for stabilization")
        elif signals.price_change_7d >= 10:
            bullets.append(f"Strong 7-day rally ({signals.price_change_7d:+.1f}%) — caution on chasing")

    # Data limitation effect
    if data_limited:
        bullets.append("News/sentiment data limited — bias reduced by one step for risk management")

    return bullets[:4]  # Max 4 bullets


def build_invalidation_triggers(
    signals: AllocationSignals,
    final_bias: str
) -> list[str]:
    """Build the invalidation trigger bullets based on current bias."""
    triggers = []

    # For accumulative biases, focus on downside triggers
    if final_bias in ("Accumulate", "Light Accumulate"):
        if signals.sma_20 is not None:
            triggers.append(f"Daily close below SMA20 at {format_price(signals.sma_20)}")
        if signals.support_1 is not None:
            triggers.append(f"Break below support at {format_price(signals.support_1)}")
        elif signals.sma_50 is not None:
            triggers.append(f"Break below SMA50 at {format_price(signals.sma_50)}")
        if signals.rsi_14 is not None:
            triggers.append("RSI < 45 sustained for 2+ days")

    # For defensive biases, focus on recovery triggers too
    elif final_bias in ("Hold", "Pause"):
        if signals.sma_50 is not None:
            triggers.append(f"Failure to reclaim SMA50 at {format_price(signals.sma_50)}")
        if signals.support_1 is not None:
            triggers.append(f"Break below support at {format_price(signals.support_1)}")
        if signals.rsi_14 is not None:
            triggers.append("RSI dropping below 30 (oversold panic)")

    # Ensure at least 2 triggers
    if len(triggers) < 2:
        if signals.current_price is not None:
            weekly_drop_level = signals.current_price * 0.9
            triggers.append(f"Price drop >10% from current ({format_price(weekly_drop_level)})")

    return triggers[:3]  # Max 3 triggers


def build_next_check_bullets(
    signals: AllocationSignals,
    final_bias: str
) -> list[str]:
    """Build the 'Next Check' bullets."""
    bullets = ["Next weekly run"]

    # What to watch based on bias
    if final_bias == "Accumulate":
        if signals.resistance_1 is not None:
            bullets.append(f"Watch for breakout above {format_price(signals.resistance_1)}")
        else:
            bullets.append("Watch for continued momentum and volume confirmation")
    elif final_bias == "Light Accumulate":
        if signals.sma_20 is not None:
            bullets.append(f"Watch for reclaim of SMA20 at {format_price(signals.sma_20)}")
        else:
            bullets.append("Watch for stabilization and support holding")
    elif final_bias == "Hold":
        if signals.sma_50 is not None:
            bullets.append(f"Watch for reclaim of SMA50 at {format_price(signals.sma_50)}")
        else:
            bullets.append("Watch for trend reversal signals")
    elif final_bias == "Pause":
        bullets.append("Watch for capitulation and volume spike for potential bottom")

    # Add data availability note if relevant
    if not signals.news_available or not signals.sentiment_available:
        bullets.append("Check if news/sentiment data availability restored")

    return bullets[:2]  # Max 2 bullets


def calculate_allocation_guidance(signals: AllocationSignals) -> AllocationGuidance:
    """
    Main function to calculate weekly allocation guidance from signals.

    This is deterministic: same inputs always produce same outputs.
    """
    # Step 1: Determine structure
    structure = determine_structure(
        signals.current_price,
        signals.sma_20,
        signals.sma_50
    )

    # Step 2: Determine RSI regime
    rsi_regime = determine_rsi_regime(signals.rsi_14)

    # Step 3: Check if key support broken
    support_broken = is_key_support_broken(
        signals.current_price,
        signals.support_1,
        signals.sma_50
    )

    # Step 4: Calculate base bias
    base_bias = calculate_base_bias(structure, rsi_regime, support_broken)

    # Step 5: Check data limitation
    data_limited = not signals.news_available or not signals.sentiment_available

    # Step 6: Apply data limitation downgrade
    if data_limited:
        final_bias = downgrade_bias(base_bias)
    else:
        final_bias = base_bias

    # Step 7: Map to allocation hint
    allocation_hint = bias_to_allocation_hint(final_bias)

    # Step 8: Build explanation bullets
    why_bullets = build_why_bullets(signals, structure, rsi_regime, data_limited, final_bias)
    invalidation_triggers = build_invalidation_triggers(signals, final_bias)
    next_check_bullets = build_next_check_bullets(signals, final_bias)

    return AllocationGuidance(
        action_bias=final_bias,
        allocation_hint=allocation_hint,
        time_horizon="1 week",
        why_bullets=why_bullets,
        invalidation_triggers=invalidation_triggers,
        next_check_bullets=next_check_bullets,
    )


def build_weekly_allocation_guidance_markdown(signals: AllocationSignals) -> str:
    """
    Build the Weekly Allocation Guidance section as Notion-friendly markdown.

    Args:
        signals: AllocationSignals dataclass with price/technical data

    Returns:
        Markdown string for the section
    """
    guidance = calculate_allocation_guidance(signals)

    # Build markdown with proper spacing for Notion rendering
    lines = [
        "### 🧭 Weekly Allocation Guidance",
        f"**Action Bias**: {guidance.action_bias}",
        f"**Allocation Hint**: {guidance.allocation_hint} of weekly DCA",
        f"**Time Horizon**: {guidance.time_horizon}",
        "",
        "**Why**",
        "",  # Blank line after header for proper list rendering
    ]

    for bullet in guidance.why_bullets:
        lines.append(f"- {bullet}")

    lines.append("")
    lines.append("**Invalidation Triggers**")
    lines.append("")  # Blank line after header for proper list rendering

    for trigger in guidance.invalidation_triggers:
        lines.append(f"- {trigger}")

    lines.append("")
    lines.append("**Next Check**")
    lines.append("")  # Blank line after header for proper list rendering

    for check in guidance.next_check_bullets:
        lines.append(f"- {check}")

    return "\n".join(lines)
