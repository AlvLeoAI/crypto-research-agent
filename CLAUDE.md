# Crypto Research Agent - Project Context

## Project Overview

An AI-powered cryptocurrency research agent that combines Claude's intelligence with a skills-based architecture, parallel subagents, and MCP integrations.

**Author:** Alvaro Leopoldo Vazquez (alvaroleopoldovazquez@gmail.com)
**GitHub:** https://github.com/AlvLeoAI

## Current Status: WORKING ✅

The agent is fully functional with:
- Live price data from CoinGecko
- Parallel subagent execution
- Report synthesis
- Notion integration for saving reports
- **Weekly Allocation Guidance** - Deterministic DCA recommendations

### Last Test (2026-02-03)
```
BTC: $78,824 (+1.62% 24h, -10.65% 7d)
RSI: 57.63 | Trend: Strong Uptrend
Weekly Allocation: Accumulate (100% of weekly DCA)
Successfully saved to Notion!
```

## Architecture

```
User Input → Main Agent (orchestrator)
                │
                ├── price_analyst    → CoinGecko MCP (LIVE DATA ✅)
                ├── news_aggregator  → Web Search (real-time news)
                └── social_sentinel  → Web Search (sentiment data)
                │
                ▼
            Synthesis + Allocation Guidance → Report → Terminal / File / Notion
                            │
                            └── 🧭 Weekly Allocation Guidance (deterministic)
```

## Project Structure

```
crypto_research_agent/
├── src/
│   ├── agent.py                 # Main orchestrator
│   ├── subagents/               # 3 specialized agents
│   ├── utils/                   # display.py, prompts.py, allocation_guidance.py
│   └── mcp/                     # Legacy (moved to mcp_servers/)
├── mcp_servers/
│   ├── coingecko/               # ✅ Working - live price data
│   │   ├── client.py
│   │   ├── server.py
│   │   └── tools.py
│   └── notion/                  # ✅ Working - saves reports
│       ├── client.py
│       ├── server.py
│       └── tools.py
├── .claude/skills/              # 4 research skills
│   ├── crypto-research-methodology/
│   ├── technical-analysis/
│   ├── news-research/
│   └── sentiment-analysis/
├── prompts/                     # 4 agent prompts
├── docs/                        # Architecture, Skills, API Setup
├── examples/                    # Sample reports
└── tests/                       # pytest tests
```

## What's Working

1. **CoinGecko MCP** - Fetches live prices, calculates RSI/SMA
2. **Notion MCP** - Saves reports with Token, Confidence, Sentiment properties
3. **Parallel Subagents** - All 3 run concurrently
4. **Report Synthesis** - Combines findings into formatted report
5. **Rich Terminal UI** - Beautiful output with panels and tables
6. **Weekly Allocation Guidance** - Deterministic DCA recommendations based on technical signals

### Weekly Allocation Guidance (NEW)

The report now includes a "🧭 Weekly Allocation Guidance" section with:
- **Action Bias**: Pause / Hold / Light Accumulate / Accumulate
- **Allocation Hint**: 0% / 25% / 50% / 100% of weekly DCA
- **Why**: 2-4 bullets explaining the decision
- **Invalidation Triggers**: 2-3 conditions that would change the recommendation
- **Next Check**: What to watch for next week

**Decision Logic:**
| Structure | RSI | Data | Bias | Allocation |
|-----------|-----|------|------|------------|
| Bullish (price > SMA20 > SMA50) | Neutral/Positive | OK | Accumulate | 100% |
| Bullish | Low | OK | Light Accumulate | 50% |
| Warning (price > SMA50, < SMA20) | Neutral | OK | Light Accumulate | 50% |
| Risk-off (price < SMA50) | Any | OK | Hold | 25% |
| Risk-off + Support Broken | Any | OK | Pause | 0% |

**Data Limitation:** If news/sentiment unavailable, bias is downgraded by 1 step.

## Environment Setup

```bash
cd ~/Projects/crypto_research_agent
source .venv/bin/activate
```

### .env Configuration
- `ANTHROPIC_API_KEY` - ✅ Set
- `COINGECKO_API_KEY` - Optional (free tier works)
- `NOTION_API_KEY` - ✅ Set
- `NOTION_DATABASE_ID` - ✅ Set (2fcc423cdaef80f18c3ddf7aeb921955)

## Running the Agent

```bash
# Interactive mode
python -m src.agent

# Direct test
python -c "
import asyncio
from src.agent import research_token
from src.utils.display import print_header, print_report

async def test():
    print_header()
    report = await research_token('bitcoin')
    print_report(report)

asyncio.run(test())
"
```

## Known Issues / Limitations

1. **Rate Limits** - Anthropic API has 30K tokens/min limit. Running all 3 subagents + synthesis can hit this. Wait 60s between runs if needed.

2. **News/Sentiment Data** - Uses web search which may occasionally be rate-limited. When unavailable:
   - Allocation guidance automatically downgrades bias by 1 step
   - Report indicates data limitation in the "Why" section

3. **Notion Properties** - Database needs these select properties:
   - Token, Confidence (High/Medium/Low), Sentiment (Bullish/Neutral/Bearish), Date

## Potential Next Steps

1. **Add Slack MCP** - Send alerts to Slack channel
2. **Reduce Token Usage** - Use Haiku for subagents to avoid rate limits
3. **Add More Tokens** - Extend TOKEN_ID_MAP in coingecko client
4. **Scheduled Research** - Cron job for daily/weekly reports
5. **Portfolio Mode** - Research multiple tokens at once
6. **Historical Tracking** - Compare reports over time
7. **Allocation Confidence** - Add numeric confidence to allocation guidance

## Key Files to Know

| File | Purpose |
|------|---------|
| `src/agent.py` | Main orchestrator, CLI loop |
| `src/utils/allocation_guidance.py` | Deterministic weekly allocation logic |
| `src/subagents/price_analyst.py` | Technical analysis, returns signals dict |
| `mcp_servers/coingecko/client.py` | CoinGecko API client |
| `mcp_servers/notion/client.py` | Notion API client |
| `.claude/skills/*/SKILL.md` | Research methodologies |
| `prompts/*.md` | Agent system prompts |
| `tests/test_allocation_guidance.py` | 42 tests for allocation logic |

## Commands Cheat Sheet

```bash
# Run agent
python -m src.agent

# Test CoinGecko
python -c "
import asyncio
from mcp_servers.coingecko import CoinGeckoClient
async def test():
    async with CoinGeckoClient() as c:
        p = await c.get_price('bitcoin')
        print(f'BTC: \${p.current_price_usd:,.0f}')
asyncio.run(test())
"

# Test Notion
python -c "
import asyncio
from mcp_servers.notion import NotionMCPHandler
async def test():
    h = NotionMCPHandler()
    print('Configured:', h.is_configured)
asyncio.run(test())
"

# Run tests
pytest -v
```

---
*Last updated: 2026-02-03*
