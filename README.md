# Crypto Research Agent

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Anthropic Claude](https://img.shields.io/badge/Powered%20by-Claude-blueviolet)](https://www.anthropic.com/)

An AI-powered cryptocurrency research agent that combines **Claude's intelligence** with a **skills-based architecture**, **parallel subagents**, and **MCP integrations** to deliver comprehensive market analysis.

![Demo](examples/demo.gif)

## Features

- **Multi-Agent Architecture** - Specialized subagents for price analysis, news aggregation, and sentiment tracking
- **Skills System** - Modular, reusable research methodologies stored as markdown
- **Parallel Execution** - All subagents run simultaneously for fast research
- **Rich Terminal UI** - Beautiful, formatted reports in your terminal
- **MCP Ready** - Designed for Model Context Protocol integrations (CoinGecko, Notion, Slack)
- **Extensible** - Easy to add new skills, subagents, or data sources

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER INPUT                                     │
│                        "research bitcoin"                                │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        MAIN AGENT (Orchestrator)                         │
│                                                                          │
│  • Loads crypto-research-methodology skill                               │
│  • Parses user request                                                   │
│  • Coordinates subagents                                                 │
│  • Synthesizes final report                                              │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────────┐
│   PRICE     │ │    NEWS     │ │    SOCIAL       │
│  ANALYST    │ │ AGGREGATOR  │ │   SENTINEL      │
├─────────────┤ ├─────────────┤ ├─────────────────┤
│ technical-  │ │ news-       │ │ sentiment-      │
│ analysis    │ │ research    │ │ analysis        │
│ skill       │ │ skill       │ │ skill           │
├─────────────┤ ├─────────────┤ ├─────────────────┤
│ • Price     │ │ • Headlines │ │ • Fear & Greed  │
│ • RSI, SMA  │ │ • Sources   │ │ • Twitter/Reddit│
│ • Support/  │ │ • Categories│ │ • Sentiment     │
│   Resistance│ │ • Red flags │ │   cycle         │
└──────┬──────┘ └──────┬──────┘ └────────┬────────┘
       │               │                  │
       └───────────────┼──────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         SYNTHESIS ENGINE                                 │
│                                                                          │
│  • Identifies agreements across sources                                  │
│  • Flags contradictions                                                  │
│  • Assesses confidence level                                             │
│  • Generates structured report                                           │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        FORMATTED REPORT                                  │
│                                                                          │
│  📊 Price Analysis    📰 News Digest    🌐 Sentiment Overview            │
│                                                                          │
│                     🔮 Synthesis & Outlook                               │
│                     ⚠️  Risk Factors                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Anthropic API key

### Installation

```bash
# Clone the repository
git clone https://github.com/AlvLeoAI/crypto-research-agent.git
cd crypto-research-agent

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# For development
uv pip install -e ".[dev]"
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_key_here
```

### Run

```bash
# Start the interactive CLI
crypto-research

# Or run directly
python -m src.agent
```

## Usage

```
>>> research bitcoin

Researching BITCOIN...

→ Dispatching research subagents in parallel...
  📊 price_analyst: Analyzing bitcoin price and technicals
  📰 news_aggregator: Gathering bitcoin news and developments
  🌐 social_sentinel: Assessing bitcoin market sentiment
  ✓ price_analysis complete (1,247 chars)
  ✓ news_analysis complete (1,532 chars)
  ✓ sentiment_analysis complete (1,189 chars)

→ Synthesizing research findings...

╭──────────────────── Research Report ────────────────────╮
│                                                          │
│  # BTC Research Report                                   │
│  **Bitcoin** | Generated 2024-01-15 14:30 UTC           │
│                                                          │
│  ## 📊 Executive Summary                                 │
│  ...                                                     │
│                                                          │
╰──────────────────────────────────────────────────────────╯
```

## Project Structure

```
crypto-research-agent/
├── src/
│   ├── agent.py                 # Main orchestrator
│   ├── subagents/               # Specialized analysis agents
│   │   ├── price_analyst.py
│   │   ├── news_aggregator.py
│   │   └── social_sentinel.py
│   ├── utils/                   # Helpers
│   │   ├── display.py           # Rich terminal formatting
│   │   └── prompts.py           # Prompt loader
│   └── mcp/                     # MCP integrations
│       └── coingecko.py         # Price data API
│
├── .claude/skills/              # Reusable research methodologies
│   ├── crypto-research-methodology/
│   ├── technical-analysis/
│   ├── news-research/
│   └── sentiment-analysis/
│
├── prompts/                     # Agent system prompts
│   ├── main_agent.md
│   ├── price_analyst.md
│   ├── news_aggregator.md
│   └── social_sentinel.md
│
├── docs/                        # Documentation
├── examples/                    # Example outputs
└── tests/                       # Test suite
```

## Skills System

Skills are modular, reusable research methodologies stored as markdown files. Each skill contains:

- **SKILL.md** - Main workflow and instructions
- **references/** - Supporting documentation
- **scripts/** - Helper scripts (optional)

See [docs/SKILLS.md](docs/SKILLS.md) for details on how skills work.

## MCP Integrations

The agent is designed for Model Context Protocol (MCP) integrations:

| Integration | Purpose | Status |
|-------------|---------|--------|
| CoinGecko | Real-time price data | Ready |
| Notion | Save reports to workspace | Planned |
| Slack | Send alerts | Planned |

See [docs/API_SETUP.md](docs/API_SETUP.md) for configuration.

## Docker

```bash
# Build the image
docker build -t crypto-research-agent .

# Run with docker-compose
docker-compose up
```

## Development

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Lint code
ruff check src/

# Type check
mypy src/
```

## Example Reports

- [Bitcoin Research](examples/bitcoin_research.md)
- [Ethereum Research](examples/ethereum_research.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Claude](https://www.anthropic.com/claude) by Anthropic
- Terminal UI powered by [Rich](https://github.com/Textualize/rich)
- Inspired by the potential of AI agents and multi-agent systems

---

**Note**: This is a portfolio project demonstrating AI agent architecture patterns. Always do your own research before making any financial decisions.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/AlvLeoAI">Alvaro Leopoldo Vazquez</a>
</p>
