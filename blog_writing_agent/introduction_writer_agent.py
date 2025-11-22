"""
Introduction Writer sub-agent for Blog Writing system.

This agent handles Step 2: writing the introduction section and establishing
the article framework based on the article plan.
"""

import json
from pathlib import Path
from google.adk.agents import LlmAgent
from utils.storage import create_markdown_storage_callback


def _load_article_plan() -> str:
    """Load the article plan from the JSON file."""
    data_dir = Path("data/collections")
    article_plan_path = data_dir / "article_plan.json"
    
    if not article_plan_path.exists():
        return "[Article plan file not found. Please run the Article Planner Agent first.]"
    
    try:
        with open(article_plan_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Extract the actual plan from the output field
            plan_data = data.get("output", data)
            # Convert back to JSON string for embedding in instruction
            return json.dumps(plan_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"[Error loading article plan: {e}]"


# Load article plan at module level
_article_plan_content = _load_article_plan()


introduction_writer_agent = LlmAgent(
    name="introduction_writer",
    model="gemini-2.5-flash-lite",
    description=(
        "Creates compelling introduction sections and establishes article framework "
        "based on the article plan. Sets the stage for the entire article with engaging "
        "hooks, context, and clear structure."
    ),
    instruction=(
        "You are the Introduction Writer Agent. Your task is to create a compelling "
        "introduction section and establish the article framework based on the provided article plan.\n\n"
        
        "## Input: Article Plan\n\n"
        "You have access to the article plan created by the Article Planner Agent:\n"
        f"{_article_plan_content}\n\n"
        
        "## Your Task\n\n"
        "Create an introduction section that:\n"
        "1. **Captures Attention**: Opens with a compelling hook that draws readers in\n"
        "2. **Establishes Context**: Provides necessary background and context for the topic\n"
        "3. **Defines Key Concepts**: Introduces and distinguishes key concepts or terms as needed\n"
        "4. **Sets Expectations**: Clearly outlines what the article will cover and its value\n"
        "5. **Creates Framework**: Establishes the structure and flow that the article will follow\n"
        "6. **Addresses Target Audience**: Speaks directly to the intended audience identified in the plan\n\n"
        
        "## Introduction Requirements\n\n"
        "### Content Elements\n"
        "- **Hook**: An engaging opening that captures interest (question, statistic, story, or provocative statement)\n"
        "- **Context Setting**: Brief background that helps readers understand the topic's relevance\n"
        "- **Problem/Opportunity**: Identify the challenge, opportunity, or question the article addresses\n"
        "- **Key Definitions**: If needed, clearly define important terms or concepts that will be used throughout\n"
        "- **Article Roadmap**: Preview the main sections and what readers will learn\n"
        "- **Value Proposition**: Reinforce why this article is worth reading\n\n"
        
        "### Framework Establishment\n"
        "The introduction should establish a clear framework that:\n"
        "- Outlines the logical flow of the article\n"
        "- Sets up the key themes that will be explored\n"
        "- Introduces the differentiation strategy (if applicable)\n"
        "- Creates anticipation for the insights to come\n\n"
        
        "### Writing Guidelines\n"
        "- **Tone**: Match the professional tone specified in the article plan\n"
        "- **Accessibility**: Balance technical depth with accessibility as specified\n"
        "- **Length**: Aim for the estimated word count in the introduction section plan\n"
        "- **Engagement**: Use active voice, clear transitions, and compelling language\n"
        "- **Evidence**: Incorporate any evidence needs identified for the introduction (anecdotes, trends, etc.)\n"
        "- **Examples**: Include practical examples if specified in the plan\n"
        "- **Distinctions**: Make any conceptual distinctions identified in the plan\n\n"
        
        "## Output Format\n\n"
        "Produce your introduction as well-formatted markdown that includes:\n"
        "- A clear heading (e.g., '# Introduction' or similar)\n"
        "- Proper paragraph structure with clear transitions\n"
        "- Any subheadings if the introduction has multiple parts\n"
        "- Professional formatting ready for publication\n\n"
        
        "## Key Considerations\n\n"
        "1. **Alignment with Plan**: Ensure the introduction aligns with the article overview, "
        "target audience, and key message from the plan\n"
        "2. **Differentiation**: Incorporate the differentiation strategy naturally into the introduction\n"
        "3. **Flow**: Create a smooth transition that leads readers into the main content\n"
        "4. **Completeness**: The introduction should feel complete while setting up the rest of the article\n"
        "5. **Engagement**: Prioritize reader engagement and value from the first sentence\n\n"
        
        "Review the article plan carefully and create a compelling introduction that establishes "
        "the framework for the entire article. Make it engaging, informative, and aligned with "
        "the plan's objectives."
    ),
    output_key="introduction_section",
    after_agent_callback=create_markdown_storage_callback("introduction_section"),
)

