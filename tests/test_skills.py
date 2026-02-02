"""
Tests for the skills system.

Tests skill loading, structure validation, and reference file access.
"""

import pytest
from pathlib import Path


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def skills_dir():
    """Return the skills directory path."""
    return Path(".claude/skills")


@pytest.fixture
def all_skills():
    """Return list of all skill names."""
    return [
        "crypto-research-methodology",
        "technical-analysis",
        "news-research",
        "sentiment-analysis",
    ]


# =============================================================================
# Skill Structure Tests
# =============================================================================

class TestSkillStructure:
    """Tests for skill directory structure."""

    def test_skills_directory_exists(self, skills_dir):
        """Skills directory should exist."""
        assert skills_dir.exists(), f"Skills directory not found: {skills_dir}"

    def test_all_skills_exist(self, skills_dir, all_skills):
        """All expected skills should have directories."""
        for skill_name in all_skills:
            skill_path = skills_dir / skill_name
            assert skill_path.exists(), f"Skill not found: {skill_name}"
            assert skill_path.is_dir(), f"Skill should be a directory: {skill_name}"

    def test_all_skills_have_skill_md(self, skills_dir, all_skills):
        """Each skill should have a SKILL.md file."""
        for skill_name in all_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            assert skill_md.exists(), f"SKILL.md not found for: {skill_name}"

    def test_all_skills_have_references(self, skills_dir, all_skills):
        """Each skill should have a references directory."""
        for skill_name in all_skills:
            refs_dir = skills_dir / skill_name / "references"
            assert refs_dir.exists(), f"references/ not found for: {skill_name}"
            assert refs_dir.is_dir(), f"references should be a directory: {skill_name}"


# =============================================================================
# Skill Content Tests
# =============================================================================

class TestSkillContent:
    """Tests for skill file content."""

    def test_skill_md_has_frontmatter(self, skills_dir, all_skills):
        """Each SKILL.md should have YAML frontmatter."""
        for skill_name in all_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            content = skill_md.read_text()

            assert content.startswith("---"), f"SKILL.md should start with --- for: {skill_name}"
            # Check for closing frontmatter
            lines = content.split("\n")
            frontmatter_closes = any(line == "---" for line in lines[1:20])
            assert frontmatter_closes, f"SKILL.md frontmatter not closed for: {skill_name}"

    def test_skill_md_has_required_sections(self, skills_dir, all_skills):
        """Each SKILL.md should have key sections."""
        required_sections = ["## Overview", "## When to Use"]

        for skill_name in all_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            content = skill_md.read_text()

            for section in required_sections:
                assert section in content, f"Missing '{section}' in {skill_name}/SKILL.md"

    def test_skill_frontmatter_has_name(self, skills_dir, all_skills):
        """Frontmatter should contain name field."""
        for skill_name in all_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            content = skill_md.read_text()

            assert "name:" in content, f"Frontmatter missing 'name:' in {skill_name}"

    def test_skill_frontmatter_has_description(self, skills_dir, all_skills):
        """Frontmatter should contain description field."""
        for skill_name in all_skills:
            skill_md = skills_dir / skill_name / "SKILL.md"
            content = skill_md.read_text()

            assert "description:" in content, f"Frontmatter missing 'description:' in {skill_name}"


# =============================================================================
# Reference Files Tests
# =============================================================================

class TestReferenceFiles:
    """Tests for skill reference files."""

    def test_crypto_research_has_template(self, skills_dir):
        """crypto-research-methodology should have report-template.md."""
        ref_file = skills_dir / "crypto-research-methodology/references/report-template.md"
        assert ref_file.exists(), "report-template.md not found"

        content = ref_file.read_text()
        assert len(content) > 100, "report-template.md seems too short"

    def test_technical_analysis_has_indicators(self, skills_dir):
        """technical-analysis should have indicators.md."""
        ref_file = skills_dir / "technical-analysis/references/indicators.md"
        assert ref_file.exists(), "indicators.md not found"

        content = ref_file.read_text()
        assert "RSI" in content, "indicators.md should mention RSI"
        assert "SMA" in content or "Moving Average" in content, "indicators.md should mention moving averages"

    def test_news_research_has_sources(self, skills_dir):
        """news-research should have trusted-sources.md."""
        ref_file = skills_dir / "news-research/references/trusted-sources.md"
        assert ref_file.exists(), "trusted-sources.md not found"

        content = ref_file.read_text()
        assert "Tier" in content, "trusted-sources.md should have tier system"

    def test_sentiment_analysis_has_rules(self, skills_dir):
        """sentiment-analysis should have sentiment-rules.md."""
        ref_file = skills_dir / "sentiment-analysis/references/sentiment-rules.md"
        assert ref_file.exists(), "sentiment-rules.md not found"

        content = ref_file.read_text()
        assert "Fear" in content and "Greed" in content, "sentiment-rules.md should mention Fear & Greed"


# =============================================================================
# Script Tests
# =============================================================================

class TestSkillScripts:
    """Tests for skill helper scripts."""

    def test_calculate_indicators_exists(self, skills_dir):
        """technical-analysis should have calculate_indicators.py."""
        script = skills_dir / "technical-analysis/scripts/calculate_indicators.py"
        assert script.exists(), "calculate_indicators.py not found"

    def test_calculate_indicators_is_valid_python(self, skills_dir):
        """calculate_indicators.py should be valid Python."""
        script = skills_dir / "technical-analysis/scripts/calculate_indicators.py"
        content = script.read_text()

        # Try to compile (doesn't execute, just checks syntax)
        try:
            compile(content, script, "exec")
        except SyntaxError as e:
            pytest.fail(f"calculate_indicators.py has syntax error: {e}")

    def test_calculate_indicators_has_rsi_function(self, skills_dir):
        """calculate_indicators.py should have RSI calculation."""
        script = skills_dir / "technical-analysis/scripts/calculate_indicators.py"
        content = script.read_text()

        assert "def calculate_rsi" in content, "Missing calculate_rsi function"

    def test_calculate_indicators_has_sma_function(self, skills_dir):
        """calculate_indicators.py should have SMA calculation."""
        script = skills_dir / "technical-analysis/scripts/calculate_indicators.py"
        content = script.read_text()

        assert "def calculate_sma" in content, "Missing calculate_sma function"


# =============================================================================
# Prompt Loader Tests
# =============================================================================

class TestPromptLoader:
    """Tests for prompt loading utility."""

    def test_prompts_directory_exists(self):
        """Prompts directory should exist."""
        prompts_dir = Path("prompts")
        assert prompts_dir.exists(), "prompts/ directory not found"

    def test_all_prompts_exist(self):
        """All expected prompts should exist."""
        expected = [
            "main_agent.md",
            "price_analyst.md",
            "news_aggregator.md",
            "social_sentinel.md",
        ]
        prompts_dir = Path("prompts")

        for prompt_file in expected:
            path = prompts_dir / prompt_file
            assert path.exists(), f"Prompt not found: {prompt_file}"

    def test_load_prompt_function(self):
        """load_prompt function should work."""
        from src.utils.prompts import load_prompt

        prompt = load_prompt("main_agent")
        assert len(prompt) > 100, "main_agent prompt seems too short"
        assert "Research Orchestrator" in prompt or "orchestrat" in prompt.lower()

    def test_load_prompt_missing_file(self):
        """load_prompt should raise error for missing file."""
        from src.utils.prompts import load_prompt

        with pytest.raises(FileNotFoundError):
            load_prompt("nonexistent_prompt")

    def test_get_available_prompts(self):
        """get_available_prompts should return all prompt names."""
        from src.utils.prompts import get_available_prompts

        prompts = get_available_prompts()
        assert "main_agent" in prompts
        assert "price_analyst" in prompts
        assert len(prompts) >= 4


# =============================================================================
# Integration Tests
# =============================================================================

class TestSkillIntegration:
    """Integration tests for skill loading in agents."""

    def test_skill_loading_in_price_analyst(self):
        """price_analyst should be able to load its skill."""
        from src.subagents.price_analyst import load_skill_content

        skill, indicators = load_skill_content()
        assert len(skill) > 100, "Skill content too short"
        assert len(indicators) > 100, "Indicators reference too short"

    def test_skill_loading_in_news_aggregator(self):
        """news_aggregator should be able to load its skill."""
        from src.subagents.news_aggregator import load_skill_content

        skill, sources = load_skill_content()
        assert len(skill) > 100, "Skill content too short"
        assert len(sources) > 100, "Sources reference too short"

    def test_skill_loading_in_social_sentinel(self):
        """social_sentinel should be able to load its skill."""
        from src.subagents.social_sentinel import load_skill_content

        skill, rules = load_skill_content()
        assert len(skill) > 100, "Skill content too short"
        assert len(rules) > 100, "Rules reference too short"
