# MCP Servers

This directory contains Model Context Protocol (MCP) servers that provide external data access to the Crypto Research Agent.

## Available Servers

### CoinGecko MCP Server

Provides cryptocurrency market data from the CoinGecko API.

#### Tools

| Tool | Description |
|------|-------------|
| `get_crypto_price` | Get current price, market cap, volume, and changes for a token |
| `get_historical_prices` | Get historical price data for technical analysis (RSI, MAs) |
| `get_market_overview` | Get total market cap, BTC dominance, market-wide stats |
| `search_tokens` | Search for tokens by name or symbol |
| `get_trending_tokens` | Get currently trending cryptocurrencies |

#### Usage

**Direct usage in Python:**

```python
from mcp_servers.coingecko import CoinGeckoMCPHandler

async def main():
    handler = CoinGeckoMCPHandler()
    
    # Get Bitcoin price
    result = await handler.handle_tool_call(
        "get_crypto_price",
        {"token": "BTC"}
    )
    print(result)
    
    # Get historical data
    historical = await handler.handle_tool_call(
        "get_historical_prices",
        {"token": "ethereum", "days": 14}
    )
    print(historical)
    
    await handler.close()
```

**As standalone MCP server:**

```bash
# Run the server (communicates via stdio)
python -m mcp_servers.coingecko.server
```

---

### Notion MCP Server

Saves crypto research reports to a Notion database.

#### Tools

| Tool | Description |
|------|-------------|
| `save_report_to_notion` | Save a research report with token, confidence, sentiment |
| `search_notion_reports` | Search for existing reports in the workspace |

#### Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Create a database with these properties:
   - **Name** (title) - Auto-populated with report title
   - **Token** (select) - Cryptocurrency symbol
   - **Confidence** (select) - High/Medium/Low
   - **Sentiment** (select) - Bullish/Neutral/Bearish
   - **Date** (date) - Report timestamp
3. Share the database with your integration
4. Add to your `.env`:

```
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

#### Usage

```python
from mcp_servers.notion import NotionMCPHandler

async def main():
    handler = NotionMCPHandler()
    
    result = await handler.handle_tool_call(
        "save_report_to_notion",
        {
            "token": "BTC",
            "report_content": "# Bitcoin Report\n\nAnalysis here...",
            "confidence": "High",
            "sentiment": "Bullish"
        }
    )
    print(result)  # {"success": True, "url": "https://notion.so/..."}
    
    await handler.close()
```

---

**Configure in Claude Desktop:**

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "coingecko": {
      "command": "python",
      "args": ["-m", "mcp_servers.coingecko.server"],
      "cwd": "/path/to/crypto_research_agent"
    }
  }
}
```

#### API Key (Optional)

The free CoinGecko API has rate limits. For higher limits, get a Pro API key:

1. Sign up at https://www.coingecko.com/en/api/pricing
2. Add to your `.env` file:

```
COINGECKO_API_KEY=CG-xxxxxxxxxxxxxxxxxxxxx
```

#### Supported Tokens

The client includes a symbol-to-ID mapping for common tokens:

```
BTC, ETH, SOL, ADA, DOT, AVAX, MATIC, LINK, UNI, ATOM,
XRP, DOGE, SHIB, LTC, BCH, NEAR, APT, ARB, OP, SUI, 
SEI, TIA, INJ, FET, RNDR, GRT, FIL, AAVE, MKR, CRV,
LDO, RPL, SNX, COMP, PEPE, WIF, BONK, FLOKI
```

For other tokens, use the `search_tokens` tool to find the correct ID.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Application                     │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │              CoinGeckoMCPHandler                    ││
│  │                                                      ││
│  │  handle_tool_call(name, args) ──────────────────┐   ││
│  │                                                  │   ││
│  │  ┌─────────────────┐    ┌────────────────────┐  │   ││
│  │  │  Tool Definitions│    │  CoinGeckoClient  │◄─┘   ││
│  │  │  (tools.py)      │    │  (client.py)      │      ││
│  │  └─────────────────┘    └────────────────────┘      ││
│  │                                   │                  ││
│  └───────────────────────────────────┼──────────────────┘│
│                                      │                   │
└──────────────────────────────────────┼───────────────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │   CoinGecko API     │
                            │   (api.coingecko.com)│
                            └─────────────────────┘
```

## Adding New MCP Servers

To add a new MCP server:

1. Create a new directory: `mcp_servers/new_server/`
2. Implement:
   - `client.py` - API client for the external service
   - `tools.py` - MCP tool definitions
   - `server.py` - MCP handler and optional stdio server
   - `__init__.py` - Package exports
3. Add to `mcp_servers/__init__.py`
4. Update the agent to use the new tools

## Testing

```bash
# Test CoinGecko client directly
python -c "
import asyncio
from mcp_servers.coingecko import CoinGeckoClient

async def test():
    async with CoinGeckoClient() as client:
        price = await client.get_price('bitcoin')
        print(f'BTC: \${price.current_price_usd:,.2f}')

asyncio.run(test())
"
```