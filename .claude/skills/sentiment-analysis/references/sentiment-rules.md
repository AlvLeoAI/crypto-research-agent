# Sentiment Analysis Rules & Framework

## The Fear & Greed Index

### How It's Calculated

The Crypto Fear & Greed Index (0-100) typically aggregates:

| Component | Weight | Measures |
|-----------|--------|----------|
| Volatility | 25% | Current vs 30/90-day averages |
| Market Momentum/Volume | 25% | Current vs 30/90-day averages |
| Social Media | 15% | Twitter engagement, hashtags |
| Surveys | 15% | Polling data (when available) |
| Bitcoin Dominance | 10% | BTC % of total market cap |
| Google Trends | 10% | Search interest for crypto terms |

### Historical Context

| Index | Historical Frequency | Typical Outcome |
|-------|---------------------|-----------------|
| 0-10 | Rare (<5% of time) | Often near cycle bottoms |
| 11-25 | ~15% of time | Accumulation zones |
| 26-45 | ~25% of time | Recovery/uncertainty |
| 46-55 | ~20% of time | Neutral, trend continuation |
| 56-74 | ~25% of time | Bull runs, optimism |
| 75-90 | ~10% of time | Late-stage rallies |
| 91-100 | Rare (<5% of time) | Often near cycle tops |

### Using the Index

**DO:**
- Use as one input among many
- Note the trend direction (rising/falling fear)
- Consider how long it's been extreme
- Compare to price action (divergences are notable)

**DON'T:**
- Trade solely based on F&G readings
- Expect immediate reversals at extremes
- Ignore context of broader market conditions
- Assume it applies equally to all tokens

---

## Social Sentiment Patterns

### The Sentiment Cycle

```
                    EUPHORIA (Peak)
                        🔺
                       /  \
                      /    \
         EXCITEMENT /      \ ANXIETY
                   /        \
                  /          \
       OPTIMISM /            \ DENIAL
               /              \
              /                \
    HOPE ←────                  ────→ FEAR
              \                /
               \              /
        RELIEF  \            / CAPITULATION
                 \          /
                  \        /
         DISBELIEF \      / DEPRESSION
                    \    /
                     \  /
                      \/
                DESPONDENCY (Bottom)
```

### Identifying Cycle Position

**Accumulation Phase (Post-bottom):**
- Low social volume
- Skepticism dominates
- "Smart money" accumulating quietly
- Few new retail participants

**Early Bull (Hope/Optimism):**
- Increasing social activity
- Mix of skepticism and optimism
- Quality discussions about fundamentals
- Gradual price recovery

**Mid Bull (Excitement):**
- Rising social volume
- FOMO beginning
- New participants entering
- Media coverage increasing

**Late Bull (Euphoria):**
- Maximum social activity
- "Can't lose" mentality
- Everyone talking about crypto
- Price targets become outlandish
- Quality of discussion declines

**Early Bear (Anxiety/Denial):**
- "Buy the dip" everywhere
- Dismissing negative news
- Still high social activity
- Nervousness creeping in

**Mid Bear (Fear/Capitulation):**
- Blame and anger
- Selling pressure
- Declining engagement
- "Told you so" crowd appears

**Late Bear (Depression/Despondency):**
- Minimal social activity
- Abandonment of projects
- "Crypto is dead" articles
- Only true believers remain

---

## Platform-Specific Signals

### Twitter/X Signals

| Signal | Interpretation |
|--------|----------------|
| Trending hashtags | High attention (not always bullish) |
| Influencer consensus | Often contrarian indicator |
| Engagement > followers | Organic interest |
| Sudden follower spikes | Potential bot activity |
| Thread quality declining | Late-stage sentiment |

### Reddit Signals

| Signal | Interpretation |
|--------|----------------|
| DD posts increasing | Early interest, research phase |
| Memes dominating | Late-stage, FOMO driven |
| "When moon" posts | Retail FOMO, caution |
| Technical discussion | Healthy community |
| Infighting/drama | Community stress |
| Mod removals increasing | Potential issues being suppressed |

### YouTube Signals

| Signal | Interpretation |
|--------|----------------|
| View counts spiking | Retail attention high |
| Clickbait thumbnails | Late-stage FOMO |
| "I was wrong" videos | Sentiment shifting |
| Tutorial content | Adoption phase |
| Outrage content | Controversial event |

---

## Contrarian Framework

### When to Consider Contrarian Positions

**Potential Buy Signals (Contrarian):**
- Fear & Greed < 20 for extended period
- Social volume at multi-month lows
- "Crypto is dead" in mainstream media
- Long-term holders not selling despite price drop
- Development activity continues despite price

**Potential Sell Signals (Contrarian):**
- Fear & Greed > 80 for extended period
- Social volume at all-time highs
- Mainstream media covering crypto positively
- Retail stories everywhere ("my barber bought...")
- Development activity slowing, focus on marketing

### Contrarian Caveats

- Markets can stay irrational longer than you can stay solvent
- Sentiment extremes are necessary but not sufficient conditions
- Always use with price action and fundamental analysis
- Contrarian doesn't mean "always fade the crowd"

---

## Manipulation Awareness

### Common Manipulation Tactics

| Tactic | How to Detect |
|--------|---------------|
| Bot armies | Repetitive language, coordinated timing |
| Paid shills | Sudden appearance, no history, uniform messaging |
| Fake volume | Social activity doesn't match price action |
| Coordinate raids | Sudden swarm of negative/positive posts |
| Influencer pumps | Paid promotion disclosed (or not) |

### Red Flags

- New accounts with high activity
- Copy-paste responses
- Unrealistic claims without evidence
- Aggressive attacks on skeptics
- Sudden narrative shifts

---

## Quantifying Sentiment

### Sentiment Scoring

Rate each platform on -2 to +2 scale:

| Score | Label | Description |
|-------|-------|-------------|
| +2 | Very Bullish | Unanimous optimism, high activity |
| +1 | Bullish | Generally positive, growing interest |
| 0 | Neutral | Mixed or minimal discussion |
| -1 | Bearish | Generally negative, declining interest |
| -2 | Very Bearish | Capitulation signs, abandonment |

### Aggregate Sentiment

```
Overall = (Twitter × 0.4) + (Reddit × 0.3) + (Fear&Greed × 0.3)

Where Fear&Greed normalized to -2 to +2:
  0-20   = -2
  21-40  = -1
  41-60  = 0
  61-80  = +1
  81-100 = +2
```

This gives weighted overall sentiment score for reporting.