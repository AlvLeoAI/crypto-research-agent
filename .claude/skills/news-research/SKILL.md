---
name: news-research
description: Use for aggregating and analyzing cryptocurrency news, project updates, and market developments. Filters reliable sources and assesses news sentiment.
---

# News Research Skill

## Overview

This skill guides the collection and analysis of cryptocurrency news, filtering for relevance and reliability while assessing overall news sentiment.

## When to Use

- Gathering recent news about a cryptocurrency
- Researching project developments and updates
- Understanding market-moving events
- Assessing news-based sentiment

## Research Workflow

### Step 1: Search for News

Use WebSearch with these query patterns (in order of priority):

1. `"[TOKEN NAME]" cryptocurrency news [current month] [year]`
2. `[TOKEN SYMBOL] crypto latest developments`
3. `[TOKEN NAME] blockchain update announcement`

Execute 2-3 searches to ensure coverage.

### Step 2: Filter Sources

Consult `references/trusted-sources.md` for source reliability tiers.

**Include only:**
- Tier 1 (Official) sources: Always include
- Tier 2 (Major Media) sources: Include with attribution
- Tier 3 (Crypto Native) sources: Include, note potential bias

**Exclude:**
- Tier 4 (Unverified) sources: Skip unless no other coverage
- Obvious promotional content
- Articles older than 30 days (unless historically significant)

### Step 3: Extract Key Information

For each relevant article, extract:

```
- Headline
- Source name
- Publication date
- Key points (2-3 bullets max)
- Sentiment: [Positive / Negative / Neutral]
- Significance: [High / Medium / Low]
```

### Step 4: Categorize News

Group news into categories:

| Category | Examples |
|----------|----------|
| **Protocol Updates** | Upgrades, forks, technical changes |
| **Partnerships** | Integrations, collaborations, business deals |
| **Regulatory** | Legal news, compliance, government actions |
| **Adoption** | New use cases, user growth, institutional interest |
| **Market Events** | Listings, delistings, whale movements |
| **Team/Governance** | Leadership changes, DAO votes, controversies |

### Step 5: Assess Overall News Sentiment

Based on collected news, rate sentiment:

| Rating | Criteria |
|--------|----------|
| **Very Positive** | Multiple significant positive developments, no negatives |
| **Positive** | More positive than negative, no critical issues |
| **Neutral** | Mixed or routine news, no strong directional signal |
| **Negative** | More negative than positive, concerning developments |
| **Very Negative** | Critical issues, regulatory threats, security incidents |

### Step 6: Generate Output

```markdown
## News Analysis: [TOKEN]

### Recent Headlines

1. **[Headline]** - [Source] ([Date])
   - [Key point]
   - Sentiment: [Rating] | Significance: [Level]

2. **[Headline]** - [Source] ([Date])
   - [Key point]
   - Sentiment: [Rating] | Significance: [Level]

[Continue for top 3-5 stories]

### News by Category
- **Protocol**: [Summary or "No recent news"]
- **Partnerships**: [Summary or "No recent news"]
- **Regulatory**: [Summary or "No recent news"]
- **Adoption**: [Summary or "No recent news"]

### Overall News Sentiment
[Rating] - [2-3 sentence explanation]

### Key Developments to Watch
- [Development 1 and why it matters]
- [Development 2 and why it matters]
```

## Recency Weighting

Prioritize recent news:

| Age | Weight | Notes |
|-----|--------|-------|
| < 24 hours | Very High | Breaking news, prioritize |
| 1-3 days | High | Recent and relevant |
| 3-7 days | Medium | Include if significant |
| 7-30 days | Low | Only major events |
| > 30 days | Skip | Unless historically critical |

## Red Flags

Flag and highlight any news involving:

- 🚨 Security breaches or hacks
- 🚨 Regulatory enforcement actions
- 🚨 Team departures or internal conflicts
- 🚨 Significant token unlocks or selling
- 🚨 Smart contract vulnerabilities
- 🚨 Exchange delistings

## Error Handling

| Scenario | Action |
|----------|--------|
| No news found | Report "No significant news in past 30 days" |
| Only low-tier sources | Include with caveat about source quality |
| Paywalled articles | Use headline and available summary only |
| Contradictory reports | Note the contradiction, cite both sources |