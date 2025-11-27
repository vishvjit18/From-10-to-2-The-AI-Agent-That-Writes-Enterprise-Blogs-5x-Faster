"""
Introduction Writer sub-agent for Blog Writing system.

This agent handles Step 2: writing the introduction section and establishing
the article framework based on the article plan.

Uses dynamic instruction generation to receive only filtered, relevant parts
of the article plan, improving token efficiency and focus.
"""

import json

from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext
from utils.retry import gemini_model
from utils.storage import create_markdown_storage_callback
from .plan_filters import _load_article_plan, filter_for_introduction


async def _instruction_provider(context: ReadonlyContext) -> str:
    """
    Dynamically generate instruction with filtered article plan context.
    
    This function is called at runtime to build the instruction with only
    the relevant parts of the article plan for the Introduction Writer.
    """
    # Load and filter article plan
    article_plan = _load_article_plan()
    
    if not article_plan:
        # Handle missing article plan gracefully
        return (
            "You are the Introduction Writer Agent. However, the article plan file "
            "was not found. Please ensure the Article Planner Agent has been run first."
        )
    
    filtered_context = filter_for_introduction(article_plan)
    
    # Convert filtered context to JSON string for embedding in instruction
    filtered_json = json.dumps(filtered_context, indent=2, ensure_ascii=False)
    
    # Build dynamic instruction with filtered context
    instruction = (
        "You are the Introduction Writer Agent. Your task is to create a compelling "
        "introduction section and establish the article framework based on the provided article plan.\n\n"
        
        "## Input: Filtered Article Plan Context\n\n"
        "You have access to the following relevant parts of the article plan:\n"
        f"{filtered_json}\n\n"
        
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
        "- **Tone and Style**: Follow the professional tone and technical accessibility balance specified in the article plan context above\n"
        "- **Length**: Aim for the estimated word count specified in the introduction section plan\n"
        "- **Engagement**: Use active voice, clear transitions, and compelling language\n"
        "- **Evidence**: Incorporate the evidence needs identified in the introduction section plan\n"
        "- **Examples**: Include the practical examples specified in the introduction section plan\n"
        "- **Distinctions**: Make the conceptual distinctions identified in the introduction section plan\n\n"
        
        "## Target Audience and Context\n\n"
        "Ensure your introduction aligns with the 'overview' section in the article plan context above, "
        "particularly the target audience, key message, purpose, and differentiation strategy.\n\n"
        
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
        
        "Review the filtered article plan context carefully and create a compelling introduction that establishes "
        "the framework for the entire article. Make it engaging, informative, and aligned with "
        "the plan's objectives."
    )
    
    return instruction

introduction_writer_agent = LlmAgent(
    name="introduction_writer",
    model=gemini_model,
    description=(
        "Creates compelling introduction sections and establishes article framework "
        "based on filtered article plan context. Sets the stage for the entire article with engaging "
        "hooks, context, and clear structure."
    ),
    instruction=_instruction_provider,  # Dynamic instruction provider
    output_key="introduction_section",
    after_agent_callback=create_markdown_storage_callback("introduction_section"),
)

