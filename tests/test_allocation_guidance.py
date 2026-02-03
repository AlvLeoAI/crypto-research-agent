"""
Tests for Weekly Allocation Guidance module.

Tests the deterministic logic that generates allocation guidance from technical signals.
"""

import pytest
from src.utils.allocation_guidance import (
    AllocationSignals,
    AllocationGuidance,
    determine_structure,
    determine_rsi_regime,
    is_key_support_broken,
    calculate_base_bias,
    downgrade_bias,
    bias_to_allocation_hint,
    calculate_allocation_guidance,
    build_weekly_allocation_guidance_markdown,
)


# =============================================================================
# Structure Determination Tests
# =============================================================================

class TestDetermineStructure:
    """Tests for price structure determination."""

    def test_bullish_structure_price_above_both_sma(self):
        """Price > SMA50 AND Price > SMA20 should be bullish."""
        assert determine_structure(100, 95, 90) == "bullish"
        assert determine_structure(50000, 48000, 45000) == "bullish"

    def test_warning_structure_price_above_sma50_below_sma20(self):
        """Price > SMA50 AND Price <= SMA20 should be warning."""
        assert determine_structure(95, 100, 90) == "warning"
        assert determine_structure(48000, 50000, 45000) == "warning"

    def test_risk_off_structure_price_below_sma50(self):
        """Price <= SMA50 should be risk_off."""
        assert determine_structure(85, 90, 90) == "risk_off"
        assert determine_structure(90, 95, 90) == "risk_off"
        assert determine_structure(44000, 50000, 45000) == "risk_off"

    def test_unknown_structure_missing_data(self):
        """Missing price or SMA50 should return unknown."""
        assert determine_structure(None, 95, 90) == "unknown"
        assert determine_structure(100, 95, None) == "unknown"
        assert determine_structure(None, None, None) == "unknown"

    def test_bullish_structure_missing_sma20(self):
        """Price > SMA50 with missing SMA20 should default to bullish."""
        assert determine_structure(100, None, 90) == "bullish"


# =============================================================================
# RSI Regime Tests
# =============================================================================

class TestDetermineRsiRegime:
    """Tests for RSI momentum regime determination."""

    def test_rsi_low_below_45(self):
        """RSI < 45 should be low."""
        assert determine_rsi_regime(44) == "low"
        assert determine_rsi_regime(30) == "low"
        assert determine_rsi_regime(0) == "low"

    def test_rsi_neutral_between_45_and_60(self):
        """45 <= RSI <= 60 should be neutral."""
        assert determine_rsi_regime(45) == "neutral"
        assert determine_rsi_regime(52) == "neutral"
        assert determine_rsi_regime(60) == "neutral"

    def test_rsi_positive_above_60(self):
        """RSI > 60 should be positive."""
        assert determine_rsi_regime(61) == "positive"
        assert determine_rsi_regime(70) == "positive"
        assert determine_rsi_regime(100) == "positive"

    def test_rsi_unknown_missing_data(self):
        """Missing RSI should return unknown."""
        assert determine_rsi_regime(None) == "unknown"


# =============================================================================
# Support Break Tests
# =============================================================================

class TestIsSupportBroken:
    """Tests for key support break detection."""

    def test_support_broken_below_support_1(self):
        """Price below support_1 should indicate broken support."""
        assert is_key_support_broken(85, 90, 80) is True

    def test_support_intact_above_support_1(self):
        """Price above support_1 should indicate intact support."""
        assert is_key_support_broken(95, 90, 80) is False

    def test_support_broken_below_sma50_when_no_support_1(self):
        """Price below SMA50 with no support_1 should indicate broken support."""
        assert is_key_support_broken(85, None, 90) is True

    def test_support_intact_when_no_support_data(self):
        """Missing price should return False (conservative)."""
        assert is_key_support_broken(None, 90, 80) is False
        assert is_key_support_broken(100, None, None) is False


# =============================================================================
# Base Bias Calculation Tests
# =============================================================================

class TestCalculateBaseBias:
    """Tests for base action bias calculation."""

    def test_bullish_neutral_rsi_intact_support_gives_accumulate(self):
        """Bullish structure + neutral RSI + intact support -> Accumulate."""
        assert calculate_base_bias("bullish", "neutral", False) == "Accumulate"

    def test_bullish_positive_rsi_intact_support_gives_accumulate(self):
        """Bullish structure + positive RSI + intact support -> Accumulate."""
        assert calculate_base_bias("bullish", "positive", False) == "Accumulate"

    def test_bullish_low_rsi_gives_light_accumulate(self):
        """Bullish structure + low RSI -> Light Accumulate."""
        assert calculate_base_bias("bullish", "low", False) == "Light Accumulate"

    def test_warning_neutral_rsi_gives_light_accumulate(self):
        """Warning structure + neutral RSI -> Light Accumulate."""
        assert calculate_base_bias("warning", "neutral", False) == "Light Accumulate"

    def test_warning_low_rsi_gives_hold(self):
        """Warning structure + low RSI -> Hold."""
        assert calculate_base_bias("warning", "low", False) == "Hold"

    def test_risk_off_no_breakdown_gives_hold(self):
        """Risk-off structure without support break -> Hold."""
        assert calculate_base_bias("risk_off", "neutral", False) == "Hold"

    def test_risk_off_with_breakdown_gives_pause(self):
        """Risk-off structure with support break -> Pause."""
        assert calculate_base_bias("risk_off", "neutral", True) == "Pause"

    def test_unknown_structure_gives_hold(self):
        """Unknown structure -> Hold (conservative default)."""
        assert calculate_base_bias("unknown", "neutral", False) == "Hold"


# =============================================================================
# Bias Downgrade Tests
# =============================================================================

class TestDowngradeBias:
    """Tests for bias downgrade due to data limitations."""

    def test_downgrade_accumulate_to_light_accumulate(self):
        """Accumulate should downgrade to Light Accumulate."""
        assert downgrade_bias("Accumulate") == "Light Accumulate"

    def test_downgrade_light_accumulate_to_hold(self):
        """Light Accumulate should downgrade to Hold."""
        assert downgrade_bias("Light Accumulate") == "Hold"

    def test_downgrade_hold_to_pause(self):
        """Hold should downgrade to Pause."""
        assert downgrade_bias("Hold") == "Pause"

    def test_downgrade_pause_stays_pause(self):
        """Pause should stay Pause (cannot go lower)."""
        assert downgrade_bias("Pause") == "Pause"


# =============================================================================
# Allocation Hint Tests
# =============================================================================

class TestBiasToAllocationHint:
    """Tests for bias to allocation hint mapping."""

    def test_pause_gives_0_percent(self):
        """Pause -> 0%."""
        assert bias_to_allocation_hint("Pause") == "0%"

    def test_hold_gives_25_percent(self):
        """Hold -> 25%."""
        assert bias_to_allocation_hint("Hold") == "25%"

    def test_light_accumulate_gives_50_percent(self):
        """Light Accumulate -> 50%."""
        assert bias_to_allocation_hint("Light Accumulate") == "50%"

    def test_accumulate_gives_100_percent(self):
        """Accumulate -> 100%."""
        assert bias_to_allocation_hint("Accumulate") == "100%"


# =============================================================================
# Integration Tests - Full Guidance Calculation
# =============================================================================

class TestCalculateAllocationGuidance:
    """Integration tests for full guidance calculation."""

    def test_fixture_a_bullish_rsi_58_data_limited(self):
        """
        Fixture A: bullish_structure + RSI ~58 + data_limited true
        -> Light Accumulate (after downgrade from Accumulate)
        """
        signals = AllocationSignals(
            current_price=80000,
            price_change_7d=-10.65,
            sma_20=77500,
            sma_50=75000,
            rsi_14=58,
            support_1=76000,
            resistance_1=82000,
            volume_status="above",
            news_available=False,  # Data limited
            sentiment_available=True,
        )

        guidance = calculate_allocation_guidance(signals)

        assert guidance.action_bias == "Light Accumulate"
        assert guidance.allocation_hint == "50%"
        assert guidance.time_horizon == "1 week"
        assert len(guidance.why_bullets) >= 2
        assert len(guidance.invalidation_triggers) >= 2

    def test_fixture_b_bullish_rsi_62_data_ok(self):
        """
        Fixture B: bullish_structure + RSI ~62 + data_ok
        -> Accumulate
        """
        signals = AllocationSignals(
            current_price=80000,
            price_change_7d=5.5,
            sma_20=77500,
            sma_50=75000,
            rsi_14=62,
            support_1=76000,
            resistance_1=82000,
            volume_status="above",
            news_available=True,
            sentiment_available=True,
        )

        guidance = calculate_allocation_guidance(signals)

        assert guidance.action_bias == "Accumulate"
        assert guidance.allocation_hint == "100%"

    def test_fixture_c_price_below_sma50_gives_hold(self):
        """
        Fixture C: price < SMA50 (risk_off structure, no support break)
        -> Hold
        """
        signals = AllocationSignals(
            current_price=74000,
            price_change_7d=-8.0,
            sma_20=77500,
            sma_50=75000,
            rsi_14=45,
            support_1=72000,  # Support intact
            resistance_1=78000,
            volume_status="below",
            news_available=True,
            sentiment_available=True,
        )

        guidance = calculate_allocation_guidance(signals)

        assert guidance.action_bias == "Hold"
        assert guidance.allocation_hint == "25%"

    def test_fixture_c_price_below_sma50_support_broken_gives_pause(self):
        """
        Fixture C variant: price < SMA50 AND support broken
        -> Pause
        """
        signals = AllocationSignals(
            current_price=71000,  # Below support
            price_change_7d=-12.0,
            sma_20=77500,
            sma_50=75000,
            rsi_14=38,
            support_1=72000,  # Support broken
            resistance_1=78000,
            volume_status="below",
            news_available=True,
            sentiment_available=True,
        )

        guidance = calculate_allocation_guidance(signals)

        assert guidance.action_bias == "Pause"
        assert guidance.allocation_hint == "0%"

    def test_determinism_same_inputs_same_outputs(self):
        """Same inputs should always produce exactly the same outputs."""
        signals = AllocationSignals(
            current_price=78824,
            price_change_7d=-10.65,
            sma_20=77500,
            sma_50=78200,
            rsi_14=57.63,
            support_1=76200,
            resistance_1=80500,
            volume_status="above",
            news_available=True,
            sentiment_available=True,
        )

        guidance1 = calculate_allocation_guidance(signals)
        guidance2 = calculate_allocation_guidance(signals)

        assert guidance1.action_bias == guidance2.action_bias
        assert guidance1.allocation_hint == guidance2.allocation_hint
        assert guidance1.why_bullets == guidance2.why_bullets
        assert guidance1.invalidation_triggers == guidance2.invalidation_triggers

    def test_minimal_data_gives_conservative_guidance(self):
        """Minimal data should give conservative (Hold) guidance."""
        signals = AllocationSignals(
            current_price=80000,
            # No other data
        )

        guidance = calculate_allocation_guidance(signals)

        # With unknown structure (no SMA50), should default to Hold
        assert guidance.action_bias == "Hold"
        assert guidance.allocation_hint == "25%"


# =============================================================================
# Markdown Output Tests
# =============================================================================

class TestBuildWeeklyAllocationGuidanceMarkdown:
    """Tests for markdown output generation."""

    def test_markdown_contains_required_labels(self):
        """Markdown should contain all required section labels."""
        signals = AllocationSignals(
            current_price=80000,
            sma_20=77500,
            sma_50=75000,
            rsi_14=58,
            news_available=True,
            sentiment_available=True,
        )

        markdown = build_weekly_allocation_guidance_markdown(signals)

        assert "### 🧭 Weekly Allocation Guidance" in markdown
        assert "**Action Bias**:" in markdown
        assert "**Allocation Hint**:" in markdown
        assert "**Time Horizon**:" in markdown
        assert "**Why**" in markdown
        assert "**Invalidation Triggers**" in markdown
        assert "**Next Check**" in markdown

    def test_markdown_contains_bullet_points(self):
        """Markdown should contain bullet points for Why/Triggers/Next."""
        signals = AllocationSignals(
            current_price=80000,
            sma_20=77500,
            sma_50=75000,
            rsi_14=58,
            news_available=True,
            sentiment_available=True,
        )

        markdown = build_weekly_allocation_guidance_markdown(signals)

        # Count bullet points (lines starting with "- ")
        bullet_count = markdown.count("\n- ")

        # Should have at least 2 Why + 2 Triggers + 1 Next = 5 bullets minimum
        assert bullet_count >= 5

    def test_markdown_shows_correct_bias_and_hint(self):
        """Markdown should show the correct bias and allocation hint."""
        # Test Accumulate case
        signals = AllocationSignals(
            current_price=80000,
            sma_20=77500,
            sma_50=75000,
            rsi_14=62,
            news_available=True,
            sentiment_available=True,
        )

        markdown = build_weekly_allocation_guidance_markdown(signals)

        assert "Accumulate" in markdown
        assert "100%" in markdown

    def test_markdown_includes_price_levels(self):
        """Markdown should include actual price levels in invalidation triggers."""
        signals = AllocationSignals(
            current_price=80000,
            sma_20=77500,
            sma_50=75000,
            rsi_14=58,
            support_1=76000,
            news_available=True,
            sentiment_available=True,
        )

        markdown = build_weekly_allocation_guidance_markdown(signals)

        # Should include SMA20 or support level in invalidation triggers
        assert "$77,500" in markdown or "$76,000" in markdown

    def test_markdown_mentions_data_limitation_when_present(self):
        """Markdown should mention data limitation in Why bullets."""
        signals = AllocationSignals(
            current_price=80000,
            sma_20=77500,
            sma_50=75000,
            rsi_14=58,
            news_available=False,  # Data limited
            sentiment_available=True,
        )

        markdown = build_weekly_allocation_guidance_markdown(signals)

        assert "data" in markdown.lower() and ("limited" in markdown.lower() or "reduced" in markdown.lower())


# =============================================================================
# Report Integration Tests
# =============================================================================

class TestReportIntegration:
    """Tests for integration with report generation."""

    def test_inject_allocation_guidance_at_correct_position(self):
        """Allocation guidance should be injected after Executive Summary."""
        from src.agent import inject_allocation_guidance

        sample_report = """# BTC Research Report
**Bitcoin** | Generated 2026-02-03 10:00 UTC

---

## 📊 Executive Summary

Bitcoin is showing strength.

**Overall Stance**: Bullish 🟢
**Confidence**: High

---

## 💰 Price Analysis

### Current Metrics
| Metric | Value |
|--------|-------|
| Price | $80,000 |
"""

        guidance_markdown = """### 🧭 Weekly Allocation Guidance
**Action Bias**: Accumulate
**Allocation Hint**: 100% of weekly DCA
**Time Horizon**: 1 week

**Why**
- Price above both SMA20 and SMA50 — bullish structure intact

**Invalidation Triggers**
- Daily close below SMA20 at $77,500

**Next Check**
- Next weekly run"""

        result = inject_allocation_guidance(sample_report, guidance_markdown)

        # Guidance should appear after Executive Summary and before Price Analysis
        exec_summary_pos = result.find("## 📊 Executive Summary")
        guidance_pos = result.find("### 🧭 Weekly Allocation Guidance")
        price_analysis_pos = result.find("## 💰 Price Analysis")

        assert exec_summary_pos < guidance_pos < price_analysis_pos

    def test_guidance_section_appears_in_final_report(self):
        """The final report should contain the allocation guidance section."""
        # This is a snapshot test - verify the section appears with correct structure
        sample_report = """# BTC Research Report

## 📊 Executive Summary
Summary here.

---

## 💰 Price Analysis
Price info here.
"""
        guidance = """### 🧭 Weekly Allocation Guidance
**Action Bias**: Hold"""

        from src.agent import inject_allocation_guidance
        result = inject_allocation_guidance(sample_report, guidance)

        assert "🧭 Weekly Allocation Guidance" in result
        assert "Action Bias" in result
