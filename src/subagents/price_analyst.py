"""
Price Analyst Subagent

Specialized agent for technical analysis, price data, and market indicators.
"""

from pathlib import Path
from anthropic import Anthropic

from src.utils.prompts import load_prompt


def load_skill_content() -> tuple[str, str]:
    """Load the technical-analysis skill and references."""
    skill_path = Path(".claude/skills/technical-analysis/SKILL.md")
    indicators_path = Path(".claude/skills/technical-analysis/references/indicators.md")
    
    skill = skill_path.read_text() if skill_path.exists() else ""
    indicators = indicators_path.read_text() if indicators_path.exists() else ""
    
    return skill, indicators


async def run_price_analyst(token: str, client: Anthropic, model: str) -> str:
    """
    Run the price analyst subagent.
    
    Args:
        token: Cryptocurrency token to analyze (e.g., "bitcoin", "ETH")
        client: Anthropic client instance
        model: Model to use for analysis
    
    Returns:
        Price analysis report as markdown string
    """
    # Load prompt and skill
    try:
        agent_prompt = load_prompt("price_analyst")
    except FileNotFoundError:
        agent_prompt = "You are a cryptocurrency price analyst."
    
    skill_content, indicators_ref = load_skill_content()
    
    # Build the system prompt with skill
    system_prompt = f"""{agent_prompt}

## Skill: technical-analysis

{skill_content}

## Reference: indicators.md

{indicators_ref}
"""
    
    # User request
    user_message = f"""Analyze {token} - provide:
1. Current price and market metrics (price, 24h change, 7d change, market cap, volume)
2. Technical indicators (RSI if calculable, trend assessment)
3. Key support and resistance levels
4. Brief technical outlook

Follow the technical-analysis skill workflow and output format exactly.

Note: You don't have direct API access in this context. Use your knowledge of current 
approximate prices, or indicate that real-time data would need to be fetched via MCP.
Provide the best analysis you can with available information."""
    
    # Call Claude
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    return response.content[0].text