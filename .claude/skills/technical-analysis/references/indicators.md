# Technical Indicators Reference

## RSI (Relative Strength Index)

### Calculation
RSI = 100 - (100 / (1 + RS))
Where RS = Average Gain / Average Loss over N periods (typically 14)

### Interpretation

| RSI Value | Interpretation | Typical Action |
|-----------|----------------|----------------|
| > 70 | Overbought | Potential pullback or reversal |
| 60-70 | Strong bullish momentum | Trend likely continues |
| 40-60 | Neutral | No clear signal |
| 30-40 | Weak bearish momentum | Watch for reversal |
| < 30 | Oversold | Potential bounce or reversal |

### Crypto-Specific Notes
- Crypto markets often sustain "overbought" readings longer than traditional markets
- RSI < 20 or > 80 are more reliable extreme signals in crypto
- Divergence (price vs RSI) is a stronger signal than absolute levels

---

## Moving Averages

### Simple Moving Average (SMA)

**SMA(20)** - Short-term trend
- Price above SMA20 = Short-term bullish
- Price below SMA20 = Short-term bearish

**SMA(50)** - Medium-term trend
- Price above SMA50 = Medium-term bullish
- Price below SMA50 = Medium-term bearish

### Golden Cross / Death Cross
- **Golden Cross**: SMA20 crosses above SMA50 → Bullish signal
- **Death Cross**: SMA20 crosses below SMA50 → Bearish signal

### Crypto-Specific Notes
- Crypto moves fast; consider using 10/30 instead of 20/50 for faster signals
- In strong trends, price may not touch moving averages for extended periods

---

## Volume Analysis

### Volume Trend

Compare current 24h volume to 7-day average:

| Volume vs Average | Interpretation |
|-------------------|----------------|
| > 150% | Significantly elevated - strong interest |
| 100-150% | Above average - moderate interest |
| 75-100% | Normal range |
| 50-75% | Below average - declining interest |
| < 50% | Low volume - potential breakout setup or disinterest |

### Volume + Price Patterns

| Price | Volume | Interpretation |
|-------|--------|----------------|
| ↑ Up | ↑ High | Strong bullish - trend confirmed |
| ↑ Up | ↓ Low | Weak bullish - potential reversal |
| ↓ Down | ↑ High | Strong bearish - trend confirmed |
| ↓ Down | ↓ Low | Weak bearish - potential reversal |

---

## Support & Resistance

### Identifying Levels

**Strong levels have multiple confluences:**
1. Previous highs/lows (tested multiple times)
2. Round numbers ($10, $100, $1000, etc.)
3. Moving average convergence
4. High volume nodes (price levels with historical high trading activity)

### Level Strength

| Touches | Strength | Notes |
|---------|----------|-------|
| 1 | Weak | Unconfirmed level |
| 2-3 | Moderate | Developing level |
| 4+ | Strong | Well-established level |

### Breakout Confirmation
A level is "broken" when:
- Price closes beyond it (not just wicks)
- Ideally with elevated volume
- Sustained for multiple candles (4h or daily)

---

## Combining Indicators

### Bullish Confluence (High Confidence Long)
- RSI rising from <30 or holding 50-60
- Price above SMA20 and SMA50
- Volume above average on up moves
- Price bouncing off support

### Bearish Confluence (High Confidence Short)
- RSI falling from >70 or holding 40-50
- Price below SMA20 and SMA50
- Volume above average on down moves
- Price rejected at resistance

### Conflicting Signals (Low Confidence)
- RSI and price direction disagreeing
- Price between moving averages
- Low volume with big price moves
- Near neither support nor resistance

---

## Crypto Market Context

Always consider broader market:

### Bitcoin Correlation
- Most altcoins correlate 60-90% with BTC
- Strong BTC move often overrides individual token technicals
- Note if token is moving independently of BTC

### Market Regime
| BTC Trend | Altcoin Strategy |
|-----------|------------------|
| Strong uptrend | Altcoins often outperform |
| Sideways | Selective altcoin moves |
| Downtrend | Most altcoins underperform BTC |

### Liquidation Levels
In leveraged crypto markets, watch for:
- Clustering of liquidations at round numbers
- Rapid moves to "hunt" liquidations
- High open interest as warning sign