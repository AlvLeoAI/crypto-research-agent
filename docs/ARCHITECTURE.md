# Architecture Overview

This document explains the system architecture of the Crypto Research Agent, including design decisions, data flow, and extension points.

## System Design

### Design Philosophy

The Crypto Research Agent follows these principles:

1. **Separation of Concerns** - Each component has a single responsibility
2. **Parallel Execution** - Subagents run concurrently for speed
3. **Skills as Configuration** - Research methodologies are externalized as markdown
4. **Progressive Disclosure** - Skills load additional context only when needed
5. **Graceful Degradation** - System continues if individual components fail

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (Rich Terminal / CLI)                        │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                        │
│                         (agent.py)                              │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Input     │  │   Skill     │  │      Synthesis          │ │
│  │   Parser    │  │   Loader    │  │       Engine            │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   PRICE ANALYST     │ │ NEWS AGGREGATOR │ │   SOCIAL SENTINEL   │
│                     │ │                 │ │                     │
│ Skill: technical-   │ │ Skill: news-    │ │ Skill: sentiment-   │
│        analysis     │ │        research │ │        analysis     │
└──────────┬──────────┘ └────────┬────────┘ └──────────┬──────────┘
           │                     │                     │
           ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  CoinGecko  │  │  WebSearch  │  │      WebFetch           │ │
│  │    MCP      │  │   (Claude)  │  │      (Claude)           │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Main Agent (Orchestrator)

**File**: `src/agent.py`

The main agent is the entry point and coordinator. It:

- Parses user input to identify the token to research
- Loads the `crypto-research-methodology` skill
- Dispatches subagents in parallel using `asyncio.gather()`
- Collects results and handles failures gracefully
- Synthesizes findings into a final report using Claude
- Renders the report with Rich formatting

**Key Functions**:

```python
async def research_token(token: str) -> str:
    """Main research workflow."""

async def run_subagents_parallel(token: str) -> dict:
    """Dispatch all subagents concurrently."""

def synthesize_report(token, results, template) -> str:
    """Combine subagent outputs into final report."""
```

### 2. Subagents

Each subagent is a specialized Claude instance with:

- A focused system prompt (from `prompts/`)
- A skill defining its methodology (from `.claude/skills/`)
- Reference materials loaded on demand

#### Price Analyst

**Files**: `src/subagents/price_analyst.py`, `prompts/price_analyst.md`

**Skill**: `technical-analysis`

**Responsibilities**:
- Fetch current price data
- Calculate technical indicators (RSI, SMA)
- Identify support/resistance levels
- Assess trend direction

#### News Aggregator

**Files**: `src/subagents/news_aggregator.py`, `prompts/news_aggregator.md`

**Skill**: `news-research`

**Responsibilities**:
- Search for recent headlines
- Filter by source reliability
- Categorize news by type
- Assess news sentiment

#### Social Sentinel

**Files**: `src/subagents/social_sentinel.py`, `prompts/social_sentinel.md`

**Skill**: `sentiment-analysis`

**Responsibilities**:
- Check Fear & Greed index
- Analyze Twitter/Reddit sentiment
- Identify sentiment cycle position
- Flag contrarian indicators

### 3. Skills System

**Location**: `.claude/skills/`

Skills are the heart of the agent's knowledge. Each skill is a directory containing:

```
skill-name/
├── SKILL.md              # Main workflow and instructions
├── references/           # Supporting documentation
│   └── reference.md
└── scripts/              # Helper scripts (optional)
    └── helper.py
```

Skills provide:
- **Workflow guidance** - Step-by-step instructions
- **Output templates** - Consistent formatting
- **Reference materials** - Domain knowledge
- **Error handling** - Graceful failure patterns

See [SKILLS.md](SKILLS.md) for details.

### 4. Utilities

#### Display (`src/utils/display.py`)

Rich-based terminal formatting with:
- Header rendering
- Status messages
- Subagent dispatch/completion indicators
- Report panels with markdown rendering
- Progress spinners

#### Prompts (`src/utils/prompts.py`)

Prompt file loader with:
- LRU caching for performance
- Error handling for missing files
- Bulk loading capability

### 5. MCP Layer

**Location**: `src/mcp/`

Model Context Protocol integrations for external data:

- **CoinGecko** (`coingecko.py`) - Price data API wrapper
- Future: Notion, Slack integrations

## Data Flow

### Research Request Flow

```
1. User Input
   │
   ├── "research bitcoin"
   │
   ▼
2. Input Parsing
   │
   ├── Token: "bitcoin"
   │
   ▼
3. Skill Loading
   │
   ├── Load crypto-research-methodology/SKILL.md
   ├── Load report-template.md
   │
   ▼
4. Parallel Dispatch
   │
   ├── Task 1: price_analyst("bitcoin")
   ├── Task 2: news_aggregator("bitcoin")
   ├── Task 3: social_sentinel("bitcoin")
   │
   ▼
5. Result Collection
   │
   ├── price_analysis: "## Price Analysis..."
   ├── news_analysis: "## News Analysis..."
   ├── sentiment_analysis: "## Sentiment..."
   │
   ▼
6. Synthesis
   │
   ├── Combine all reports
   ├── Identify agreements/contradictions
   ├── Assess confidence
   │
   ▼
7. Output
   │
   ├── Render with Rich
   └── Optional: Save to file
```

### Subagent Execution Flow

```
1. Load Agent Prompt
   │
   ├── prompts/price_analyst.md
   │
   ▼
2. Load Skill
   │
   ├── .claude/skills/technical-analysis/SKILL.md
   ├── .claude/skills/technical-analysis/references/indicators.md
   │
   ▼
3. Build System Prompt
   │
   ├── Combine prompt + skill + references
   │
   ▼
4. Call Claude API
   │
   ├── model: claude-sonnet-4-20250514
   ├── max_tokens: 2048
   │
   ▼
5. Return Result
   │
   └── Structured markdown analysis
```

## Extension Points

### Adding a New Subagent

1. Create skill in `.claude/skills/new-skill/`
2. Create prompt in `prompts/new_agent.md`
3. Create subagent in `src/subagents/new_agent.py`
4. Add to parallel dispatch in `agent.py`
5. Update synthesis prompt to include new data

### Adding a New MCP Integration

1. Create wrapper in `src/mcp/new_service.py`
2. Add environment variables to `.env.example`
3. Document in `docs/API_SETUP.md`
4. Update relevant subagent to use the integration

### Adding a New Skill

1. Create directory in `.claude/skills/`
2. Add SKILL.md with workflow
3. Add references/ with supporting docs
4. Update subagent to load the skill

## Error Handling

The system handles errors at multiple levels:

| Level | Error | Handling |
|-------|-------|----------|
| Input | Invalid token | Ask user for clarification |
| Subagent | API failure | Return error message, continue with others |
| Synthesis | Missing data | Note gap in report, proceed |
| Output | Save failure | Log error, display report anyway |

## Performance Considerations

- **Parallel Execution**: Subagents run concurrently (~3x faster than sequential)
- **Caching**: Prompt files are LRU cached
- **Token Limits**: Each subagent limited to 2048 tokens
- **Timeout Handling**: HTTP client has 30s timeout

## Security

- API keys stored in environment variables (`.env`)
- Non-root user in Docker container
- No sensitive data in logs
- Input sanitization for file paths
