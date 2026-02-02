---
name: technical-analysis
description: Use for cryptocurrency price analysis, technical indicators, support/resistance levels, and price trend assessment. Provides structured price data interpretation.
---

# Technical Analysis Skill

## Overview

This skill guides technical analysis of cryptocurrency price action, calculating key indicators and identifying important price levels.

## When to Use

- Analyzing price trends and patterns
- Calculating technical indicators (RSI, moving averages)
- Identifying support and resistance levels
- Assessing short-term price momentum

## Data Sources

### Primary: CoinGecko API (via MCP)
Use MCP tools to fetch:
- Current price and 24h/7d changes
- Market cap and volume
- Price history for calculations

### Fallback: Web Search
If MCP unavailable, search for:
- "[TOKEN] price today"
- "[TOKEN] technical analysis"

## Analysis Workflow

### Step 1: Fetch Current Data

Required metrics:
```
- current_price (USD)
- price_change_24h (%)
- price_change_7d (%)
- market_cap (USD)
- total_volume_24h (USD)
- circulating_supply
```

### Step 2: Calculate Indicators

If historical data available, run `scripts/calculate_indicators.py`:

```bash
python scripts/calculate_indicators.py --token [SYMBOL] --days 14
```

Key indicators to calculate:
- **RSI (14-period)**: Momentum oscillator
- **SMA (20, 50)**: Trend direction
- **Volume trend**: Comparing to 7-day average

See `references/indicators.md` for interpretation guidelines.

### Step 3: Identify Levels

Determine key price levels:

**Resistance levels** (prices where selling pressure expected):
- Recent local highs
- Round numbers (psychological levels)
- Previous support turned resistance

**Support levels** (prices where buying pressure expected):
- Recent local lows
- Round numbers
- Previous resistance turned support

### Step 4: Trend Assessment

Classify the trend:

| Trend | Criteria |
|-------|----------|
| **Strong Uptrend** | Price > SMA20 > SMA50, RSI 50-70 |
| **Weak Uptrend** | Price > SMA20, RSI 40-60 |
| **Sideways** | Price oscillating around SMA20, RSI 40-60 |
| **Weak Downtrend** | Price < SMA20, RSI 40-60 |
| **Strong Downtrend** | Price < SMA20 < SMA50, RSI 30-50 |

### Step 5: Generate Assessment

Produce structured output:

```markdown
## Price Analysis: [TOKEN]

### Current Metrics
- Price: $X.XX
- 24h: [+/-]X.X%
- 7d: [+/-]X.X%
- Market Cap: $X.XB
- Volume (24h): $X.XM

### Technical Indicators
- RSI (14): XX - [Interpretation]
- Trend: [Classification]
- Volume: [Above/Below] 7-day average

### Key Levels
- Resistance: $X.XX, $X.XX
- Support: $X.XX, $X.XX

### Technical Outlook
[2-3 sentences interpreting the data]
```

## Output Requirements

Always include:
1. Current price with 24h and 7d changes
2. At least one technical indicator (RSI preferred)
3. At least one support and one resistance level
4. Brief trend assessment (1-2 sentences)

## Error Handling

| Scenario | Action |
|----------|--------|
| Token not found | Return error with spelling suggestions |
| API rate limited | Use cached data if <1h old, else report unavailable |
| Insufficient history | Skip indicators, note "New token - limited history" |

## Confidence Indicators

Note data quality in output:
- **Fresh data**: Updated within 5 minutes
- **Recent data**: Updated within 1 hour
- **Stale data**: Updated >1 hour ago (flag this)