"""
News Aggregator Subagent

Specialized agent for gathering and analyzing cryptocurrency news.
Uses Anthropic's web_search tool to fetch real-time news.
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
    Run the news aggregator subagent with web search.
    
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
    
    # User request - agent will use web_search tool
    user_message = f"""Research recent news for {token}.

Use the web_search tool to find real-time news. Search for:
1. "{token} cryptocurrency news" - recent headlines
2. "{token} crypto developments" - project updates

Then analyze the results following the news-research skill:
1. Filter to reliable sources (Tier 1-3 from trusted-sources.md)
2. Categorize news by type (protocol, partnerships, regulatory, adoption)
3. Assess overall news sentiment
4. Identify key developments to watch
5. Flag any red flags or concerns

Provide your analysis in the skill's output format."""

    # Define web_search tool
    tools = [
        {
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 3  # Limit searches to control costs
        }
    ]
    
    # Call Claude with web_search tool
    messages = [{"role": "user", "content": user_message}]
    
    # Agentic loop to handle tool use
    while True:
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=messages
        )
        
        # Check if we need to process tool use
        if response.stop_reason == "tool_use":
            # Add assistant's response to messages
            messages.append({"role": "assistant", "content": response.content})
            
            # Process tool results (web_search results are handled automatically by Anthropic)
            # The model will continue with the search results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    # Web search is handled server-side, just acknowledge
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": "Search completed - results provided above."
                    })
            
            messages.append({"role": "user", "content": tool_results})
        else:
            # No more tool use, extract final text
            break
    
    # Extract text from response
    result_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            result_text += block.text
    
    return result_text if result_text else "Unable to gather news data."