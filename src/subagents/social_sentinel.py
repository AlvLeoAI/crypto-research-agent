"""
Social Sentinel Subagent

Specialized agent for analyzing market sentiment and social signals.
"""

from pathlib import Path
from anthropic import Anthropic

from src.utils.prompts import load_prompt


def load_skill_content() -> tuple[str, str]:
    """Load the sentiment-analysis skill and references."""
    skill_path = Path(".claude/skills/sentiment-analysis/SKILL.md")
    rules_path = Path(".claude/skills/sentiment-analysis/references/sentiment-rules.md")
    
    skill = skill_path.read_text() if skill_path.exists() else ""
    rules = rules_path.read_text() if rules_path.exists() else ""
    
    return skill, rules


async def run_social_sentinel(token: str, client: Anthropic, model: str) -> str:
    """
    Run the social sentinel subagent.
    
    Args:
        token: Cryptocurrency token to analyze (e.g., "bitcoin", "ETH")
        client: Anthropic client instance
        model: Model to use for analysis
    
    Returns:
        Sentiment analysis report as markdown string
    """
    # Load prompt and skill
    try:
        agent_prompt = load_prompt("social_sentinel")
    except FileNotFoundError:
        agent_prompt = "You are a cryptocurrency sentiment analyst."
    
    skill_content, rules_ref = load_skill_content()
    
    # Build the system prompt with skill
    system_prompt = f"""{agent_prompt}

## Skill: sentiment-analysis

{skill_content}

## Reference: sentiment-rules.md

{rules_ref}
"""
    
    # User request
    user_message = f"""Analyze market sentiment for {token}:
1. Assess the current Fear & Greed context
2. Evaluate Twitter/X sentiment and activity
3. Evaluate Reddit sentiment and activity
4. Identify where we are in the sentiment cycle
5. Note any contrarian indicators
6. Flag potential manipulation or warning signs

Follow the sentiment-analysis skill workflow and output format exactly.

Note: You don't have direct social media access in this context. Use your knowledge of 
general market sentiment patterns and any recent sentiment trends you're aware of. 
Indicate that real-time sentiment data would need to be fetched via WebSearch tool.
Provide the best analysis you can with available information."""
    
    # Call Claude
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    return response.content[0].text