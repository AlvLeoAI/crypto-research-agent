"""
Prompt loader utility.

Loads agent prompts from the prompts/ directory.
"""

from pathlib import Path
from functools import lru_cache


PROMPTS_DIR = Path("prompts")


@lru_cache(maxsize=10)
def load_prompt(name: str) -> str:
    """
    Load a prompt file by name.
    
    Args:
        name: Prompt name (without .md extension)
              e.g., "main_agent", "price_analyst"
    
    Returns:
        Prompt content as string
    
    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    prompt_path = PROMPTS_DIR / f"{name}.md"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    
    return prompt_path.read_text()


def load_all_prompts() -> dict[str, str]:
    """
    Load all prompt files from the prompts directory.
    
    Returns:
        Dictionary mapping prompt names to their content
    """
    prompts = {}
    
    if not PROMPTS_DIR.exists():
        return prompts
    
    for prompt_file in PROMPTS_DIR.glob("*.md"):
        name = prompt_file.stem
        prompts[name] = prompt_file.read_text()
    
    return prompts


def get_available_prompts() -> list[str]:
    """
    Get list of available prompt names.
    
    Returns:
        List of prompt names (without .md extension)
    """
    if not PROMPTS_DIR.exists():
        return []
    
    return [p.stem for p in PROMPTS_DIR.glob("*.md")]