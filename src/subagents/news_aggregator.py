"""
News Aggregator Subagent

Specialized agent for gathering and analyzing cryptocurrency news.
"""

from pathlib import Path
from anthropic import Anthropic

from src.utils.prompts import load_prompt


def load_skill_content() -> tuple[str, str]:
    """Load the news-research skill and references."""
    skill_path = Path(".claude/skills/news-research/SKILL.md")
    sources_path = Path(".claude/skills/news-research/references/trusted-sources.md")
    
    skill = skill_path.read_text() if skill_path.exists() else ""
    sources = sources_path.read_text() if sources_path.exists() else ""
    
    return skill, sources


async def run_news_aggregator(token: str, client: Anthropic, model: str) -> str:
    """
    Run the news aggregator subagent.
    
    Args:
        token: Cryptocurrency token to research (e.g., "bitcoin", "ETH")
        client: Anthropic client instance
        model: Model to use for analysis
    
    Returns:
        News analysis report as markdown string
    """
    # Load prompt and skill
    try:
        agent_prompt = load_prompt("news_aggregator")
    except FileNotFoundError:
        agent_prompt = "You are a cryptocurrency news analyst."
    
    skill_content, sources_ref = load_skill_content()
    
    # Build the system prompt with skill
    system_prompt = f"""{agent_prompt}

## Skill: news-research

{skill_content}

## Reference: trusted-sources.md

{sources_ref}
"""
    
    # User request
    user_message = f"""Research recent news for {token}:
1. Find the most significant recent headlines (past 7 days)
2. Categorize news by type (protocol, partnerships, regulatory, adoption, etc.)
3. Assess overall news sentiment
4. Identify key developments to watch
5. Flag any red flags or concerns

Follow the news-research skill workflow and output format exactly.

Note: You don't have direct web search in this context. Use your knowledge of recent 
developments and news you're aware of. Indicate that real-time news would need to be 
fetched via WebSearch tool. Provide the best analysis you can with available information."""
    
    # Call Claude
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    return response.content[0].text