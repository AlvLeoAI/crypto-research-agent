# API Setup Guide

This guide explains how to obtain and configure the API keys needed for the Crypto Research Agent.

## Required APIs

### Anthropic API (Required)

The Anthropic API powers all AI functionality in the agent.

#### Getting Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** in the sidebar
4. Click **Create Key**
5. Give your key a name (e.g., "crypto-research-agent")
6. Copy the key immediately (you won't see it again)

#### Configuration

Add to your `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxx
```

#### Pricing

- See [anthropic.com/pricing](https://www.anthropic.com/pricing) for current rates
- The agent uses Claude Sonnet by default (cost-effective)
- Typical research query: ~10-15K tokens ($0.03-0.05)

#### Rate Limits

| Tier | Requests/min | Tokens/min |
|------|--------------|------------|
| Free | 5 | 20,000 |
| Tier 1 | 50 | 40,000 |
| Tier 2 | 1,000 | 80,000 |

## Optional APIs

### CoinGecko API

Real-time cryptocurrency price data.

#### Free Tier

CoinGecko offers a free tier that works without an API key:

- 10-30 calls/minute
- Basic market data
- Sufficient for testing

#### Pro API

For production use, consider CoinGecko Pro:

1. Go to [coingecko.com/en/api/pricing](https://www.coingecko.com/en/api/pricing)
2. Choose a plan (Analyst, Lite, Pro, Enterprise)
3. Sign up and get your API key
4. Add to `.env`:

```bash
COINGECKO_API_KEY=CG-xxxxxxxxxxxxxxxx
```

#### Pricing (as of 2024)

| Plan | Price | Calls/month |
|------|-------|-------------|
| Demo | Free | 10,000 |
| Analyst | $129/mo | 500,000 |
| Lite | $499/mo | 2,000,000 |

### Notion API (Optional)

Save reports to your Notion workspace.

#### Setup

1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **New integration**
3. Name it "Crypto Research Agent"
4. Select your workspace
5. Copy the **Internal Integration Token**
6. Share your target database with the integration

#### Configuration

```bash
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Finding Database ID

1. Open your Notion database in browser
2. Copy the URL: `notion.so/workspace/DATABASE_ID?v=...`
3. The DATABASE_ID is the 32-character string before `?v=`

### Slack API (Optional)

Send research alerts to Slack.

#### Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From scratch**
3. Name it "Crypto Research Agent"
4. Select your workspace
5. Go to **OAuth & Permissions**
6. Add Bot Token Scopes:
   - `chat:write`
   - `chat:write.public`
7. Click **Install to Workspace**
8. Copy the **Bot User OAuth Token**

#### Configuration

```bash
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_CHANNEL_ID=C0XXXXXXXXX
```

#### Finding Channel ID

1. Right-click on the channel in Slack
2. Select **View channel details**
3. Scroll to the bottom to find the Channel ID

## Environment File

Your complete `.env` file should look like:

```bash
# =============================================================================
# Required
# =============================================================================
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxx

# =============================================================================
# Optional: CoinGecko
# =============================================================================
COINGECKO_API_KEY=CG-xxxxxxxxxxxxxxxx

# =============================================================================
# Optional: Model Configuration
# =============================================================================
CLAUDE_MODEL=claude-sonnet-4-20250514
SUBAGENT_MODEL=claude-sonnet-4-20250514

# =============================================================================
# Optional: Output
# =============================================================================
OUTPUT_DIR=./output
LOG_LEVEL=INFO

# =============================================================================
# Optional: Notion
# =============================================================================
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# =============================================================================
# Optional: Slack
# =============================================================================
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_CHANNEL_ID=C0XXXXXXXXX
```

## Security Best Practices

### DO:

- Store API keys in `.env` file only
- Add `.env` to `.gitignore` (already done)
- Use different keys for development and production
- Rotate keys periodically
- Set up billing alerts

### DON'T:

- Commit API keys to git
- Share keys in chat/email
- Use production keys for testing
- Embed keys in source code

## Troubleshooting

### "Invalid API Key"

- Double-check the key is copied correctly
- Ensure no extra spaces or newlines
- Verify the key hasn't been revoked

### "Rate Limit Exceeded"

- Wait a few minutes and retry
- Check your usage dashboard
- Consider upgrading your plan

### "Connection Error"

- Check your internet connection
- Verify the API endpoint is correct
- Check if the service is down

### Environment Variables Not Loading

- Ensure `.env` file is in project root
- Check file is named exactly `.env`
- Restart your terminal/IDE
- Verify `python-dotenv` is installed

## Testing Your Setup

Run this command to verify your API keys:

```bash
python -c "
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('ANTHROPIC_API_KEY', '')
if key.startswith('sk-ant'):
    print('✓ Anthropic API key configured')
else:
    print('✗ Anthropic API key missing or invalid')

if os.getenv('COINGECKO_API_KEY'):
    print('✓ CoinGecko API key configured')
else:
    print('○ CoinGecko API key not set (optional)')
"
```

Expected output:

```
✓ Anthropic API key configured
○ CoinGecko API key not set (optional)
```
