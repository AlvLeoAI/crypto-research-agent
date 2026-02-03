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

### Last Test (2026-02-02)
```
BTC: $78,824 (+1.62% 24h, -10.65% 7d)
RSI: 57.63 | Trend: Strong Uptrend
Successfully saved to Notion!
```

## Architecture

```
User Input → Main Agent (orchestrator)
                │
                ├── price_analyst    → CoinGecko MCP (LIVE DATA ✅)
                ├── news_aggregator  → Claude knowledge (needs web search)
                └── social_sentinel  → Claude knowledge (needs web search)
                │
                ▼
            Synthesis → Report → Terminal / File / Notion
```

## Project Structure

```
crypto_research_agent/
├── src/
│   ├── agent.py                 # Main orchestrator
│   ├── subagents/               # 3 specialized agents
│   ├── utils/                   # display.py, prompts.py
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

2. **News/Sentiment** - Currently use Claude's knowledge, not live web search. Could be enhanced with:
   - WebSearch tool integration
   - News API (NewsAPI, CryptoPanic)
   - Social APIs (Twitter, Reddit)

3. **Notion Properties** - Database needs these select properties:
   - Token, Confidence (High/Medium/Low), Sentiment (Bullish/Neutral/Bearish), Date

## Potential Next Steps

1. **Add WebSearch** - Real-time news and sentiment via web search
2. **Add Slack MCP** - Send alerts to Slack channel
3. **Reduce Token Usage** - Use Haiku for subagents to avoid rate limits
4. **Add More Tokens** - Extend TOKEN_ID_MAP in coingecko client
5. **Scheduled Research** - Cron job for daily reports
6. **Portfolio Mode** - Research multiple tokens at once
7. **Historical Tracking** - Compare reports over time

## Key Files to Know

| File | Purpose |
|------|---------|
| `src/agent.py` | Main orchestrator, CLI loop |
| `mcp_servers/coingecko/client.py` | CoinGecko API client |
| `mcp_servers/notion/client.py` | Notion API client |
| `.claude/skills/*/SKILL.md` | Research methodologies |
| `prompts/*.md` | Agent system prompts |

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
*Last updated: 2026-02-02*
