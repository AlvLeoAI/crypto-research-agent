"""
Tests for subagent modules.

Tests subagent initialization, prompt construction, and basic execution.
Note: Full execution tests require an API key and are marked for integration testing.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def mock_anthropic_client():
    """Create a mock Anthropic client."""
    client = Mock()

    # Mock the messages.create response
    mock_response = Mock()
    mock_response.content = [Mock(text="## Mock Analysis\n\nThis is a mock response.")]
    client.messages.create = Mock(return_value=mock_response)

    return client


@pytest.fixture
def mock_async_anthropic_client():
    """Create a mock async Anthropic client."""
    client = Mock()

    # Mock the messages.create response
    mock_response = Mock()
    mock_response.content = [Mock(text="## Mock Analysis\n\nThis is a mock response.")]
    client.messages.create = Mock(return_value=mock_response)

    return client


# =============================================================================
# Module Import Tests
# =============================================================================

class TestModuleImports:
    """Tests for subagent module imports."""

    def test_import_price_analyst(self):
        """price_analyst module should be importable."""
        from src.subagents import price_analyst
        assert hasattr(price_analyst, "run_price_analyst")

    def test_import_news_aggregator(self):
        """news_aggregator module should be importable."""
        from src.subagents import news_aggregator
        assert hasattr(news_aggregator, "run_news_aggregator")

    def test_import_social_sentinel(self):
        """social_sentinel module should be importable."""
        from src.subagents import social_sentinel
        assert hasattr(social_sentinel, "run_social_sentinel")

    def test_import_main_agent(self):
        """Main agent module should be importable."""
        from src import agent
        assert hasattr(agent, "research_token")
        assert hasattr(agent, "main")


# =============================================================================
# Skill Loading Tests
# =============================================================================

class TestSkillLoading:
    """Tests for skill loading in subagents."""

    def test_price_analyst_loads_skill(self):
        """price_analyst should load technical-analysis skill."""
        from src.subagents.price_analyst import load_skill_content

        skill, indicators = load_skill_content()

        assert "technical" in skill.lower() or "price" in skill.lower()
        assert "RSI" in indicators or "rsi" in indicators.lower()

    def test_news_aggregator_loads_skill(self):
        """news_aggregator should load news-research skill."""
        from src.subagents.news_aggregator import load_skill_content

        skill, sources = load_skill_content()

        assert "news" in skill.lower()
        assert "source" in sources.lower() or "tier" in sources.lower()

    def test_social_sentinel_loads_skill(self):
        """social_sentinel should load sentiment-analysis skill."""
        from src.subagents.social_sentinel import load_skill_content

        skill, rules = load_skill_content()

        assert "sentiment" in skill.lower()
        assert "fear" in rules.lower() or "greed" in rules.lower()


# =============================================================================
# Subagent Execution Tests (Mocked)
# =============================================================================

class TestPriceAnalyst:
    """Tests for price_analyst subagent."""

    @pytest.mark.asyncio
    async def test_run_price_analyst_returns_string(self, mock_anthropic_client):
        """run_price_analyst should return a string."""
        from src.subagents.price_analyst import run_price_analyst

        result = await run_price_analyst(
            token="bitcoin",
            client=mock_anthropic_client,
            model="claude-sonnet-4-20250514"
        )

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_run_price_analyst_calls_api(self, mock_anthropic_client):
        """run_price_analyst should call the Anthropic API."""
        from src.subagents.price_analyst import run_price_analyst

        await run_price_analyst(
            token="bitcoin",
            client=mock_anthropic_client,
            model="claude-sonnet-4-20250514"
        )

        mock_anthropic_client.messages.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_price_analyst_includes_token(self, mock_anthropic_client):
        """run_price_analyst should include token in the message."""
        from src.subagents.price_analyst import run_price_analyst

        await run_price_analyst(
            token="ethereum",
            client=mock_anthropic_client,
            model="claude-sonnet-4-20250514"
        )

        call_args = mock_anthropic_client.messages.create.call_args
        messages = call_args.kwargs.get("messages", [])

        assert any("ethereum" in str(m).lower() for m in messages)


class TestNewsAggregator:
    """Tests for news_aggregator subagent."""

    @pytest.mark.asyncio
    async def test_run_news_aggregator_returns_string(self, mock_anthropic_client):
        """run_news_aggregator should return a string."""
        from src.subagents.news_aggregator import run_news_aggregator

        result = await run_news_aggregator(
            token="bitcoin",
            client=mock_anthropic_client,
            model="claude-sonnet-4-20250514"
        )

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_run_news_aggregator_calls_api(self, mock_anthropic_client):
        """run_news_aggregator should call the Anthropic API."""
        from src.subagents.news_aggregator import run_news_aggregator

        await run_news_aggregator(
            token="bitcoin",
            client=mock_anthropic_client,
            model="claude-sonnet-4-20250514"
        )

        mock_anthropic_client.messages.create.assert_called_once()


class TestSocialSentinel:
    """Tests for social_sentinel subagent."""

    @pytest.mark.asyncio
    async def test_run_social_sentinel_returns_string(self, mock_anthropic_client):
        """run_social_sentinel should return a string."""
        from src.subagents.social_sentinel import run_social_sentinel

        result = await run_social_sentinel(
            token="bitcoin",
            client=mock_anthropic_client,
            model="claude-sonnet-4-20250514"
        )

        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_run_social_sentinel_calls_api(self, mock_anthropic_client):
        """run_social_sentinel should call the Anthropic API."""
        from src.subagents.social_sentinel import run_social_sentinel

        await run_social_sentinel(
            token="bitcoin",
            client=mock_anthropic_client,
            model="claude-sonnet-4-20250514"
        )

        mock_anthropic_client.messages.create.assert_called_once()


# =============================================================================
# Main Agent Tests
# =============================================================================

class TestMainAgent:
    """Tests for main agent module."""

    def test_load_skill(self):
        """load_skill should load SKILL.md content."""
        from src.agent import load_skill

        skill = load_skill("crypto-research-methodology")
        assert len(skill) > 100
        assert "research" in skill.lower()

    def test_load_skill_reference(self):
        """load_skill_reference should load reference files."""
        from src.agent import load_skill_reference

        template = load_skill_reference("crypto-research-methodology", "report-template.md")
        assert len(template) > 100

    def test_load_skill_missing(self):
        """load_skill should return empty string for missing skill."""
        from src.agent import load_skill

        skill = load_skill("nonexistent-skill")
        assert skill == ""

    def test_parse_token_from_input_research_command(self):
        """parse_token_from_input should handle 'research X' pattern."""
        from src.agent import parse_token_from_input

        assert parse_token_from_input("research bitcoin") == "bitcoin"
        assert parse_token_from_input("research ETH") == "ETH"
        assert parse_token_from_input("Research Solana") == "Solana"

    def test_parse_token_from_input_single_word(self):
        """parse_token_from_input should handle single token names."""
        from src.agent import parse_token_from_input

        assert parse_token_from_input("bitcoin") == "bitcoin"
        assert parse_token_from_input("ETH") == "ETH"
        assert parse_token_from_input("BTC") == "BTC"

    def test_parse_token_from_input_question(self):
        """parse_token_from_input should handle question patterns."""
        from src.agent import parse_token_from_input

        result = parse_token_from_input("what's happening with bitcoin?")
        assert result == "bitcoin"

    def test_parse_token_from_input_invalid(self):
        """parse_token_from_input should return None for invalid input."""
        from src.agent import parse_token_from_input

        result = parse_token_from_input("what is the weather today")
        assert result is None


# =============================================================================
# Utility Tests
# =============================================================================

class TestDisplayUtils:
    """Tests for display utilities."""

    def test_import_display_module(self):
        """display module should be importable."""
        from src.utils import display

        assert hasattr(display, "print_header")
        assert hasattr(display, "print_status")
        assert hasattr(display, "print_report")

    def test_console_exists(self):
        """Console instance should exist."""
        from src.utils.display import console

        assert console is not None


# =============================================================================
# CoinGecko Client Tests
# =============================================================================

class TestCoinGeckoClient:
    """Tests for CoinGecko API client."""

    def test_import_coingecko(self):
        """coingecko module should be importable."""
        from src.mcp import coingecko

        assert hasattr(coingecko, "CoinGeckoClient")
        assert hasattr(coingecko, "get_token_id")

    def test_token_id_mapping(self):
        """get_token_id should map symbols to CoinGecko IDs."""
        from src.mcp.coingecko import get_token_id

        assert get_token_id("BTC") == "bitcoin"
        assert get_token_id("ETH") == "ethereum"
        assert get_token_id("SOL") == "solana"

    def test_token_id_passthrough(self):
        """get_token_id should pass through unknown tokens."""
        from src.mcp.coingecko import get_token_id

        assert get_token_id("bitcoin") == "bitcoin"
        assert get_token_id("some-unknown-token") == "some-unknown-token"

    def test_client_initialization(self):
        """CoinGeckoClient should initialize without errors."""
        from src.mcp.coingecko import CoinGeckoClient

        client = CoinGeckoClient()
        assert client.BASE_URL == "https://api.coingecko.com/api/v3"


# =============================================================================
# Integration Tests (require API key)
# =============================================================================

@pytest.mark.integration
class TestIntegration:
    """Integration tests requiring actual API access."""

    @pytest.mark.asyncio
    async def test_full_research_flow(self):
        """Full research flow should complete without errors."""
        # This test is marked for integration testing only
        # Run with: pytest -m integration
        pytest.skip("Integration test - requires API key")
