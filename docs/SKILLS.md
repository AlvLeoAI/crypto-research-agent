# Skills System

This document explains how the skills system works in the Crypto Research Agent.

## What Are Skills?

Skills are **modular, reusable research methodologies** stored as markdown files. They provide:

- Structured workflows for specific tasks
- Domain knowledge and best practices
- Output templates for consistency
- Reference materials for deeper context

Think of skills as "instruction manuals" that teach the AI how to perform specific research tasks.

## Skill Structure

Each skill is a directory under `.claude/skills/`:

```
.claude/skills/
├── crypto-research-methodology/     # Main orchestration skill
│   ├── SKILL.md                     # Workflow and instructions
│   └── references/
│       └── report-template.md       # Output template
│
├── technical-analysis/              # Price analysis skill
│   ├── SKILL.md
│   ├── references/
│   │   └── indicators.md            # RSI, SMA interpretation
│   └── scripts/
│       └── calculate_indicators.py  # Helper calculations
│
├── news-research/                   # News aggregation skill
│   ├── SKILL.md
│   └── references/
│       └── trusted-sources.md       # Source reliability tiers
│
└── sentiment-analysis/              # Sentiment analysis skill
    ├── SKILL.md
    └── references/
        └── sentiment-rules.md       # Fear & Greed, cycles
```

### SKILL.md Format

Every skill has a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: skill-name
description: Brief description of when to use this skill
---

# Skill Title

## Overview
What this skill does and why.

## When to Use
- Trigger conditions
- User request patterns

## Workflow
Step-by-step instructions.

## Output Format
Expected output structure.

## Error Handling
How to handle edge cases.
```

### References

The `references/` directory contains supporting documentation:

- Domain knowledge
- Interpretation guides
- Templates
- Source lists

References are loaded on-demand to provide additional context.

### Scripts

Optional `scripts/` directory for helper code:

- Calculations
- Data transformations
- Validation utilities

## Skills in This Project

### 1. crypto-research-methodology

**Purpose**: Orchestrates the full research process

**Used by**: Main agent

**Key contents**:
- 4-phase research workflow
- Subagent dispatch instructions
- Synthesis guidelines
- Confidence scoring criteria

**Reference**: `report-template.md` - Full report structure

### 2. technical-analysis

**Purpose**: Price and indicator analysis

**Used by**: `price_analyst` subagent

**Key contents**:
- Data fetching workflow
- Indicator calculation steps
- Trend classification criteria
- Output format for price analysis

**Reference**: `indicators.md` - RSI, SMA, volume interpretation

**Script**: `calculate_indicators.py` - Technical calculations

### 3. news-research

**Purpose**: News gathering and assessment

**Used by**: `news_aggregator` subagent

**Key contents**:
- Search query strategies
- Source filtering workflow
- News categorization
- Sentiment assessment

**Reference**: `trusted-sources.md` - 6-tier source reliability system

### 4. sentiment-analysis

**Purpose**: Social and market sentiment

**Used by**: `social_sentinel` subagent

**Key contents**:
- Data collection sources
- Fear & Greed interpretation
- Sentiment cycle identification
- Contrarian indicators

**Reference**: `sentiment-rules.md` - Sentiment framework and patterns

## How Skills Are Loaded

### 1. Skill Loading

```python
def load_skill(skill_name: str) -> str:
    """Load a skill's SKILL.md content."""
    skill_path = Path(f".claude/skills/{skill_name}/SKILL.md")
    return skill_path.read_text()
```

### 2. Reference Loading (Progressive Disclosure)

References are loaded only when needed:

```python
def load_skill_reference(skill_name: str, reference_name: str) -> str:
    """Load a skill's reference file."""
    ref_path = Path(f".claude/skills/{skill_name}/references/{reference_name}")
    return ref_path.read_text()
```

### 3. Prompt Construction

The subagent combines its prompt with the skill:

```python
system_prompt = f"""{agent_prompt}

## Skill: {skill_name}

{skill_content}

## Reference: {reference_name}

{reference_content}
"""
```

## Benefits of Skills

### 1. Modularity

Skills can be:
- Reused across different agents
- Updated independently
- Tested in isolation

### 2. Transparency

Skills are human-readable markdown:
- Easy to understand what the agent will do
- Easy to modify behavior
- Version controllable

### 3. Progressive Disclosure

References load only when needed:
- Reduces initial context size
- Provides depth on demand
- Improves response quality

### 4. Consistency

Skills enforce:
- Standardized workflows
- Consistent output formats
- Predictable behavior

## Creating a New Skill

### Step 1: Create Directory

```bash
mkdir -p .claude/skills/my-skill/references
```

### Step 2: Create SKILL.md

```markdown
---
name: my-skill
description: Description of when to use this skill
---

# My Skill

## Overview
What this skill does.

## When to Use
- Condition 1
- Condition 2

## Workflow

### Step 1: First Step
Instructions...

### Step 2: Second Step
Instructions...

## Output Format

\`\`\`markdown
## Analysis Title

### Section 1
[Content]

### Section 2
[Content]
\`\`\`

## Error Handling

| Scenario | Action |
|----------|--------|
| Error 1 | Handle it this way |
| Error 2 | Handle it that way |
```

### Step 3: Add References (Optional)

Create files in `references/` with supporting information.

### Step 4: Add Scripts (Optional)

Create helper scripts in `scripts/` if needed.

### Step 5: Wire It Up

1. Create a subagent that loads the skill
2. Add the subagent to the orchestrator
3. Update synthesis to include new data

## Best Practices

### DO:

- Keep SKILL.md focused on workflow
- Put detailed knowledge in references
- Use tables for decision criteria
- Include example outputs
- Handle errors explicitly

### DON'T:

- Put everything in one file
- Skip the frontmatter
- Forget error handling
- Make skills too broad
- Hardcode values that might change

## Skill Interactions

Skills can reference each other:

```
crypto-research-methodology
          │
          ├── Dispatches to:
          │   ├── technical-analysis
          │   ├── news-research
          │   └── sentiment-analysis
          │
          └── Uses template from:
              └── report-template.md
```

The main skill orchestrates, while specialized skills execute.

## Future Enhancements

- **Skill discovery**: Automatic skill selection based on user intent
- **Skill chaining**: Multi-step workflows across skills
- **Skill versioning**: Track changes and rollback
- **Skill marketplace**: Share and discover community skills
