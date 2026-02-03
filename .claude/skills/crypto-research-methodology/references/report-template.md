# Research Report Template

Use this template for all cryptocurrency research reports.

## Structure

```markdown
# [TOKEN_SYMBOL] Research Report
**[TOKEN_NAME]** | Generated [YYYY-MM-DD HH:MM UTC]

---

## 📊 Executive Summary

[Maximum 3 sentences summarizing the key findings and outlook]

**Overall Stance**: [Bullish 🟢 / Neutral 🟡 / Bearish 🔴]
**Confidence**: [High / Medium / Low]

---

### 🧭 Weekly Allocation Guidance
<!-- This section is auto-generated deterministically from price signals -->
**Action Bias**: [Pause / Hold / Light Accumulate / Accumulate]
**Allocation Hint**: [0% / 25% / 50% / 100%] of weekly DCA
**Time Horizon**: 1 week

**Why**
- [2-4 bullets explaining the decision]

**Invalidation Triggers**
- [2-3 bullets with hard rules and price levels]

**Next Check**
- [1-2 bullets: next update timing and what to watch]

---

## 💰 Price Analysis

### Current Metrics
| Metric | Value |
|--------|-------|
| Price | $X.XX |
| 24h Change | +/-X.X% |
| 7d Change | +/-X.X% |
| Market Cap | $X.XB |
| 24h Volume | $X.XM |

### Technical Levels
- **Resistance**: $X.XX, $X.XX
- **Support**: $X.XX, $X.XX

### Indicators
- RSI (14): XX [Overbought >70 / Oversold <30 / Neutral]
- Trend: [Uptrend / Downtrend / Sideways]

### Price Analyst Assessment
[2-3 sentences from price_analyst subagent]

---

## 📰 News & Developments

### Recent Headlines
1. **[Headline]** - [Source] ([Date])
   - [One sentence summary]

2. **[Headline]** - [Source] ([Date])
   - [One sentence summary]

3. **[Headline]** - [Source] ([Date])
   - [One sentence summary]

### News Sentiment
[Positive / Negative / Mixed] - [Brief explanation]

### Key Developments
- [Development 1]
- [Development 2]

---

## 🌐 Market Sentiment

### Social Metrics
| Platform | Sentiment | Activity |
|----------|-----------|----------|
| Twitter/X | [Bullish/Bearish/Neutral] | [High/Medium/Low] |
| Reddit | [Bullish/Bearish/Neutral] | [High/Medium/Low] |

### Fear & Greed Context
Current Market Index: [XX] - [Extreme Fear / Fear / Neutral / Greed / Extreme Greed]

### Community Highlights
- [Notable discussion point 1]
- [Notable discussion point 2]

---

## 🔮 Synthesis & Outlook

### Agreements Across Sources
- [Point where price, news, and sentiment align]

### Contradictions to Note
- [Any conflicts between data sources]

### Short-term Outlook (1-7 days)
[Assessment based on combined analysis]

### Medium-term Outlook (1-4 weeks)
[Assessment based on combined analysis]

---

## ⚠️ Risk Factors

1. **[Risk Category]**: [Description]
2. **[Risk Category]**: [Description]
3. **[Risk Category]**: [Description]

---

## 📋 Metadata

- **Report Generated**: [Timestamp]
- **Data Sources**: [Count] sources consulted
- **Confidence Level**: [High/Medium/Low]
- **Subagents Used**: price_analyst, news_aggregator, social_sentinel

---

*This report is for informational purposes only and does not constitute financial advice.*
```

## Formatting Guidelines

1. **Use emojis sparingly** - Only in section headers for visual scanning
2. **Tables for metrics** - Easy comparison of numbers
3. **Bullet points for lists** - News, risks, developments
4. **Bold for emphasis** - Key terms and values
5. **Keep sections balanced** - No section should dominate

## Conditional Sections

- **If no news found**: Replace News section with "No significant news in the past 7 days"
- **If API data unavailable**: Note "Data temporarily unavailable" and skip metrics table
- **If sentiment unclear**: State "Insufficient data for sentiment analysis"

## Length Guidelines

| Section | Target Length |
|---------|---------------|
| Executive Summary | 3 sentences |
| Price Analysis | 100-150 words |
| News Digest | 3-5 headlines + summaries |
| Sentiment | 75-100 words |
| Synthesis | 100-150 words |
| Risks | 3-5 bullet points |