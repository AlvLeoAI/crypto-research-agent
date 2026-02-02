---
name: crypto-research-methodology
description: Use when researching cryptocurrencies, tokens, or crypto market conditions. Guides comprehensive research combining price analysis, news aggregation, and sentiment analysis into structured reports.
---

# Crypto Research Methodology

## Overview

This skill orchestrates comprehensive cryptocurrency research by coordinating specialized subagents and synthesizing their findings into actionable reports.

## When to Use

- User asks to "research" a cryptocurrency or token
- User wants market analysis or overview
- User asks about crypto news, sentiment, or price action
- User requests a report on any blockchain asset

## Research Workflow

Execute these phases in order:

### Phase 1: Parallel Data Collection

Dispatch all three subagents simultaneously:

1. **price_analyst**
   - Query: "[TOKEN] technical analysis and price levels"
   - Skill: technical-analysis

2. **news_aggregator**
   - Query: "[TOKEN] recent news and developments"
   - Skill: news-research

3. **social_sentinel**
   - Query: "[TOKEN] social sentiment and community buzz"
   - Skill: sentiment-analysis

Wait for all subagents to complete before proceeding.

### Phase 2: Synthesis

After receiving all subagent reports:

1. Identify **agreements** across sources (bullish/bearish alignment)
2. Flag **contradictions** (e.g., positive news but negative sentiment)
3. Assess **confidence level** based on data quality and consistency
4. Formulate **key takeaways** (max 5 bullet points)

### Phase 3: Report Generation

Generate report following the template in `references/report-template.md`.

Required sections:
- Executive Summary (3 sentences max)
- Price Analysis (from price_analyst)
- News Digest (from news_aggregator)
- Sentiment Overview (from social_sentinel)
- Synthesis & Outlook
- Risk Factors
- Metadata (timestamp, sources count, confidence)

### Phase 4: Output Delivery

Based on user preferences or request:

1. **Default**: Display formatted report in terminal
2. **If Notion MCP available**: Save to Notion workspace
3. **If Slack MCP available**: Send summary alert

## Confidence Scoring

Rate overall confidence as:

| Level | Criteria |
|-------|----------|
| **High** | 3+ sources agree, recent data (<24h), clear trend |
| **Medium** | Mixed signals, some data gaps, unclear trend |
| **Low** | Contradictory signals, stale data, high uncertainty |

## Error Handling

- If a subagent fails: Continue with available data, note the gap
- If all subagents fail: Report inability, suggest manual research
- If token not found: Suggest similar tokens or correct spelling

## Output Format

Always structure the final response as:

```
# [TOKEN] Research Report

## Executive Summary
[3 sentences max]

## Price Analysis
[From price_analyst subagent]

## News & Developments
[From news_aggregator subagent]

## Market Sentiment
[From social_sentinel subagent]

## Synthesis & Outlook
[Your analysis combining all sources]

## Risk Factors
[Key risks to consider]

---
Generated: [timestamp]
Confidence: [High/Medium/Low]
Sources: [count]
```
