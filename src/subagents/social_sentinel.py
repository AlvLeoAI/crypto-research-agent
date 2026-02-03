"""
Social Sentinel Subagent

Specialized agent for analyzing market sentiment and social signals.
Uses Anthropic's web_search tool to fetch real-time sentiment data.
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
    Run the social sentinel subagent with web search.
    
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
    
    # User request - agent will use web_search tool
    user_message = f"""Analyze market sentiment for {token}.

Use the web_search tool to find sentiment data. Search for:
1. "crypto fear greed index today" - get current market sentiment
2. "{token} sentiment twitter reddit" - social media sentiment

Then analyze following the sentiment-analysis skill:
1. Assess the current Fear & Greed context
2. Evaluate social media sentiment (Twitter/X, Reddit)
3. Identify where we are in the sentiment cycle
4. Note any contrarian indicators
5. Flag potential manipulation or warning signs

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
            
            # Process tool results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
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
    
    return result_text if result_text else "Unable to gather sentiment data."