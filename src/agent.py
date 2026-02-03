#!/usr/bin/env python3
"""
Crypto Research Agent - Main Orchestrator

An AI agent system that researches crypto markets using Claude,
skills, subagents, and MCP integrations.
"""

import asyncio
import os
from pathlib import Path
from datetime import datetime

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from src.utils.prompts import load_prompt
from src.utils.display import (
    print_header,
    print_status,
    print_subagent_dispatch,
    print_subagent_result,
    print_error,
    print_report,
)
from src.subagents.price_analyst import run_price_analyst
from src.subagents.news_aggregator import run_news_aggregator
from src.subagents.social_sentinel import run_social_sentinel

# Load environment variables
load_dotenv()

# Initialize
console = Console()
client = Anthropic()

# Configuration
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


def load_skill(skill_name: str) -> str:
    """Load a skill's SKILL.md content."""
    skill_path = Path(f".claude/skills/{skill_name}/SKILL.md")
    if skill_path.exists():
        return skill_path.read_text()
    return ""


def load_skill_reference(skill_name: str, reference_name: str) -> str:
    """Load a skill's reference file (progressive disclosure)."""
    ref_path = Path(f".claude/skills/{skill_name}/references/{reference_name}")
    if ref_path.exists():
        return ref_path.read_text()
    return ""


async def run_subagents_parallel(token: str) -> dict:
    """
    Dispatch all three subagents in parallel.
    
    Returns dict with results from each subagent.
    """
    print_status("Dispatching research subagents in parallel...")
    
    # Create tasks for parallel execution
    tasks = [
        asyncio.create_task(run_price_analyst(token, client, MODEL)),
        asyncio.create_task(run_news_aggregator(token, client, MODEL)),
        asyncio.create_task(run_social_sentinel(token, client, MODEL)),
    ]
    
    # Show dispatch status
    print_subagent_dispatch("price_analyst", f"Analyzing {token} price and technicals")
    print_subagent_dispatch("news_aggregator", f"Gathering {token} news and developments")
    print_subagent_dispatch("social_sentinel", f"Assessing {token} market sentiment")
    
    # Wait for all to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    subagent_results = {
        "price_analysis": results[0] if not isinstance(results[0], Exception) else f"Error: {results[0]}",
        "news_analysis": results[1] if not isinstance(results[1], Exception) else f"Error: {results[1]}",
        "sentiment_analysis": results[2] if not isinstance(results[2], Exception) else f"Error: {results[2]}",
    }
    
    # Show completion status
    for name, result in subagent_results.items():
        if isinstance(result, str) and result.startswith("Error:"):
            print_subagent_result(name, "failed", result)
        else:
            print_subagent_result(name, "complete", f"{len(result)} chars")
    
    return subagent_results


def synthesize_report(
    token: str,
    subagent_results: dict,
    report_template: str
) -> str:
    """
    Use Claude to synthesize subagent results into final report.
    """
    print_status("Synthesizing research findings...")
    
    synthesis_prompt = f"""You are synthesizing a cryptocurrency research report for {token}.

You have received analysis from three specialized subagents:

## Price Analysis (from price_analyst)
{subagent_results['price_analysis']}

## News Analysis (from news_aggregator)
{subagent_results['news_analysis']}

## Sentiment Analysis (from social_sentinel)
{subagent_results['sentiment_analysis']}

## Your Task

Synthesize these findings into a cohesive research report following this template:

{report_template}

## Synthesis Guidelines

1. **Identify agreements** - Where do price, news, and sentiment align?
2. **Flag contradictions** - Where do they conflict? Explain why.
3. **Assess confidence** - Rate High/Medium/Low based on data quality and alignment
4. **Key takeaways** - What are the 3-5 most important insights?

Generate the complete report now. Include today's date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
"""
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": synthesis_prompt}]
    )
    
    return response.content[0].text


async def research_token(token: str) -> str:
    """
    Main research workflow for a cryptocurrency token.
    
    1. Load orchestration skill
    2. Dispatch subagents in parallel
    3. Synthesize findings
    4. Return formatted report
    """
    # Load the orchestration skill
    skill_content = load_skill("crypto-research-methodology")
    report_template = load_skill_reference("crypto-research-methodology", "report-template.md")
    
    if DEBUG:
        console.print(f"[dim]Loaded skill: {len(skill_content)} chars[/dim]")
        console.print(f"[dim]Loaded template: {len(report_template)} chars[/dim]")
    
    # Run subagents in parallel
    subagent_results = await run_subagents_parallel(token)
    
    # Synthesize into final report
    report = synthesize_report(token, subagent_results, report_template)
    
    return report


def parse_token_from_input(user_input: str) -> str | None:
    """
    Extract token name/symbol from user input.
    
    Examples:
        "research bitcoin" -> "bitcoin"
        "analyze ETH" -> "ETH"
        "what's happening with solana" -> "solana"
    """
    # Common patterns
    input_lower = user_input.lower()
    
    # Direct commands
    for prefix in ["research ", "analyze ", "analyse ", "check "]:
        if input_lower.startswith(prefix):
            return user_input[len(prefix):].strip()
    
    # Question patterns
    for pattern in ["what's happening with ", "how is ", "tell me about "]:
        if pattern in input_lower:
            idx = input_lower.index(pattern) + len(pattern)
            return user_input[idx:].strip().rstrip("?")
    
    # If it's just a token name/symbol (single word, no spaces)
    if " " not in user_input.strip() and len(user_input.strip()) <= 20:
        return user_input.strip()
    
    return None


async def interactive_loop():
    """Main interactive loop for the CLI."""
    print_header()
    
    console.print(
        "\n[bold cyan]Welcome to Crypto Research Agent[/bold cyan]\n"
        "Research any cryptocurrency with AI-powered analysis.\n"
    )
    console.print(
        "[dim]Commands:[/dim]\n"
        "  • Type a token name/symbol to research (e.g., 'bitcoin', 'ETH')\n"
        "  • 'research <token>' for full analysis\n"
        "  • 'help' for more commands\n"
        "  • 'quit' or 'exit' to leave\n"
    )
    
    while True:
        try:
            user_input = console.input("\n[bold green]>>> [/bold green]").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ["quit", "exit", "q"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if user_input.lower() == "help":
                console.print(Panel(
                    "**Commands:**\n\n"
                    "• `bitcoin` or `BTC` - Research a token\n"
                    "• `research ethereum` - Full analysis\n"
                    "• `help` - Show this message\n"
                    "• `quit` - Exit the program\n\n"
                    "**Examples:**\n"
                    "• `research solana`\n"
                    "• `ETH`\n"
                    "• `what's happening with cardano`",
                    title="Help",
                    border_style="blue"
                ))
                continue
            
            # Parse token from input
            token = parse_token_from_input(user_input)
            
            if not token:
                console.print(
                    "[yellow]I couldn't understand which token to research. "
                    "Try something like 'research bitcoin' or just 'ETH'[/yellow]"
                )
                continue
            
            # Run research
            console.print(f"\n[bold]Researching {token.upper()}...[/bold]\n")
            
            report = await research_token(token)
            
            # Display report
            print_report(report)
            
            # Offer to save
            save = console.input("\n[dim]Save report? (f=file, n=notion, enter=skip): [/dim]").strip().lower()
            
            if save == "f":
                # Save to local file
                output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
                output_dir.mkdir(exist_ok=True)
                
                filename = f"{token.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                filepath = output_dir / filename
                filepath.write_text(report)
                
                console.print(f"[green]✓ Saved to {filepath}[/green]")
            
            elif save == "n":
                # Save to Notion
                try:
                    from mcp_servers.notion import NotionMCPHandler
                    
                    notion_handler = NotionMCPHandler()
                    
                    if not notion_handler.is_configured:
                        console.print(
                            "[yellow]Notion not configured. Set NOTION_API_KEY and "
                            "NOTION_DATABASE_ID in your .env file.[/yellow]"
                        )
                    else:
                        console.print("[dim]Saving to Notion...[/dim]")
                        
                        # Extract sentiment and confidence from report (simple heuristic)
                        report_lower = report.lower()
                        if "bullish" in report_lower:
                            sentiment = "Bullish"
                        elif "bearish" in report_lower:
                            sentiment = "Bearish"
                        else:
                            sentiment = "Neutral"
                        
                        if "high confidence" in report_lower:
                            confidence = "High"
                        elif "low confidence" in report_lower:
                            confidence = "Low"
                        else:
                            confidence = "Medium"
                        
                        result = await notion_handler.handle_tool_call(
                            "save_report_to_notion",
                            {
                                "token": token,
                                "report_content": report,
                                "confidence": confidence,
                                "sentiment": sentiment
                            }
                        )
                        
                        await notion_handler.close()
                        
                        if result.get("success"):
                            console.print(f"[green]✓ Saved to Notion: {result.get('url')}[/green]")
                        else:
                            console.print(f"[red]Failed: {result.get('error')}[/red]")
                            
                except ImportError:
                    console.print("[red]Notion MCP not available[/red]")
                except Exception as e:
                    console.print(f"[red]Notion error: {e}[/red]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'quit' to exit.[/yellow]")
            continue
        
        except Exception as e:
            print_error(f"An error occurred: {e}")
            if DEBUG:
                console.print_exception()
            continue


def main():
    """Entry point for the CLI."""
    try:
        asyncio.run(interactive_loop())
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")


if __name__ == "__main__":
    main()