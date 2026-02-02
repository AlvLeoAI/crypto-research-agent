---
name: sentiment-analysis
description: Use for analyzing cryptocurrency market sentiment from social media, community discussions, and market indicators like Fear & Greed index. Identifies crowd psychology and potential sentiment extremes.
---

# Sentiment Analysis Skill

## Overview

This skill guides the analysis of market sentiment through social signals, community activity, and sentiment indicators to gauge crowd psychology around a cryptocurrency.

## When to Use

- Assessing community sentiment for a token
- Identifying potential sentiment extremes (euphoria/panic)
- Understanding social momentum and buzz
- Contextualizing price action with crowd behavior

## Data Sources

### Primary Sources

1. **Crypto Fear & Greed Index**
   - Search: "crypto fear greed index today"
   - Source: alternative.me or similar aggregators
   
2. **Twitter/X Sentiment**
   - Search: "[TOKEN] twitter sentiment"
   - Search: "[TOKEN SYMBOL] crypto twitter"
   - Look for engagement metrics, trending status

3. **Reddit Activity**
   - Search: "[TOKEN] reddit cryptocurrency"
   - Check r/cryptocurrency, project-specific subs
   - Look for post frequency, upvotes, comment sentiment

### Secondary Sources

4. **Google Trends**
   - Search: "[TOKEN] google trends"
   - Compare to baseline and competitors

5. **YouTube Activity**
   - Search: "[TOKEN] youtube crypto"
   - Note: High YouTube activity often indicates retail FOMO

## Analysis Workflow

### Step 1: Gather Sentiment Data

Collect data points:

```
Fear & Greed Index: [0-100]
Twitter Sentiment: [Bullish/Bearish/Neutral]
Twitter Activity: [High/Medium/Low]
Reddit Sentiment: [Bullish/Bearish/Neutral]
Reddit Activity: [High/Medium/Low]
Search Interest: [Rising/Stable/Declining]
```

### Step 2: Interpret Fear & Greed

Consult `references/sentiment-rules.md` for interpretation framework.

| Index Value | Label | Interpretation |
|-------------|-------|----------------|
| 0-24 | Extreme Fear | Potential buying opportunity (contrarian) |
| 25-44 | Fear | Market pessimistic, watch for reversal |
| 45-55 | Neutral | No clear sentiment signal |
| 56-74 | Greed | Market optimistic, caution advised |
| 75-100 | Extreme Greed | Potential top, high risk (contrarian) |

### Step 3: Assess Social Activity

Rate activity level:

| Metric | High | Medium | Low |
|--------|------|--------|-----|
| Twitter mentions/day | >1000 | 100-1000 | <100 |
| Reddit posts/week | >50 | 10-50 | <10 |
| YouTube videos/week | >20 | 5-20 | <5 |

### Step 4: Identify Sentiment Patterns

Look for these patterns:

**🟢 Bullish Signals:**
- Rising social volume + positive sentiment
- Increasing search interest
- Influential accounts accumulating
- Constructive technical discussions

**🔴 Bearish Signals:**
- Declining engagement despite news
- Capitulation posts ("I give up")
- Influencers turning negative
- Support-seeking posts increasing

**⚠️ Warning Signs (Potential Tops):**
- "Everyone" talking about the token
- Price target posts everywhere
- Mainstream media coverage spike
- "Easy money" / "Can't lose" posts
- Extreme greed on index

**⚠️ Warning Signs (Potential Bottoms):**
- Community abandonment
- "Crypto is dead" sentiment
- Extreme fear on index
- Long-term holders capitulating
- No one discussing the token

### Step 5: Contrarian Assessment

Evaluate contrarian indicators:

| Crowd Behavior | Contrarian View |
|----------------|-----------------|
| Maximum euphoria | Potential top forming |
| Maximum despair | Potential bottom forming |
| Consensus bullish | Risk of reversal |
| Consensus bearish | Risk of reversal |

### Step 6: Generate Output

```markdown
## Sentiment Analysis: [TOKEN]

### Market Sentiment Indicators

| Indicator | Value | Signal |
|-----------|-------|--------|
| Fear & Greed Index | [XX] | [Label] |
| Twitter Sentiment | [Rating] | [Volume] activity |
| Reddit Sentiment | [Rating] | [Volume] activity |
| Search Trend | [Direction] | [Context] |

### Social Activity Summary

**Twitter/X:**
- Sentiment: [Bullish/Neutral/Bearish]
- Key narratives: [What people are discussing]
- Notable accounts: [Any influential voices]

**Reddit:**
- Sentiment: [Bullish/Neutral/Bearish]
- Community mood: [Description]
- Hot topics: [Current discussions]

### Sentiment Assessment

**Overall Sentiment**: [Bullish/Neutral/Bearish]
**Sentiment Strength**: [Strong/Moderate/Weak]

[2-3 sentence summary of sentiment landscape]

### Contrarian Indicators

- [Any extreme readings or warning signs]
- [Potential contrarian opportunities]

### Crowd Psychology Notes

[Brief assessment of where we are in the sentiment cycle]
```

## Important Caveats

Always include in output:

1. **Sentiment ≠ Price Direction** - Sentiment can stay extreme longer than expected
2. **Manipulation Risk** - Social metrics can be gamed (bots, paid shills)
3. **Lag Effect** - Sentiment often follows price, not predicts it
4. **Sample Bias** - Social platforms skew younger and more speculative

## Error Handling

| Scenario | Action |
|----------|--------|
| No social data found | Report "Insufficient social data" |
| Token too new | Note "Limited sentiment history" |
| Conflicting signals | Report the conflict, don't force a conclusion |
| Obvious manipulation | Flag as "Potentially manipulated metrics" |