"""
Subagents package.

Specialized agents for different aspects of crypto research:
- price_analyst: Technical analysis and price data
- news_aggregator: News gathering and assessment
- social_sentinel: Sentiment analysis
"""

from src.subagents.price_analyst import run_price_analyst
from src.subagents.news_aggregator import run_news_aggregator
from src.subagents.social_sentinel import run_social_sentinel

__all__ = [
    "run_price_analyst",
    "run_news_aggregator",
    "run_social_sentinel",
]
