"""
Conclusion Writer sub-agent for Blog Writing system.

This agent handles writing the conclusion and synthesis section of the article,
based on the structured article plan.

Uses dynamic instruction generation to receive only filtered, relevant parts
of the article plan, improving token efficiency and focus.
"""

import json

from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext

from utils.retry import gemini_model
from utils.storage import create_markdown_storage_callback
from .plan_filters import _load_article_plan, filter_for_conclusion_writer


async def _instruction_provider(context: ReadonlyContext) -> str:
    """
    Dynamically generate instruction with filtered article plan context.

    This function is called at runtime to build the instruction with only
    the relevant parts of the article plan for the Conclusion Writer.
    """
    # Load and filter article plan
    article_plan = _load_article_plan()

    if not article_plan:
        # Handle missing article plan gracefully
        return (
            "You are the Conclusion Writer Agent. However, the article plan file "
            "was not found. Please ensure the Article Planner Agent has been run first."
        )

    filtered_context = filter_for_conclusion_writer(article_plan)

    # Convert filtered context to JSON string for embedding in instruction
    filtered_json = json.dumps(filtered_context, indent=2, ensure_ascii=False)

    # Build dynamic instruction with filtered context
    instruction = (
        "You are the Conclusion Writer Agent. Your task is to write a strong, "
        "memorable conclusion that synthesizes the article's key ideas and leaves "
        "the reader with clear takeaways and a forward-looking perspective.\n\n"

        "## Input: Filtered Article Plan Context\n\n"
        "You have access to the following relevant parts of the article plan:\n"
        f"{filtered_json}\n\n"

        "## Your Task\n\n"
        "Create a conclusion section that:\n"
        "1. **Synthesizes Key Ideas**: Pulls together the most important points from the article into a coherent summary\n"
        "2. **Reinforces the Key Message**: Clearly restates the core message and value proposition\n"
        "3. **Highlights Impact**: Emphasizes why the topic matters and what changes or outcomes it can drive\n"
        "4. **Connects Back to the Reader**: Speaks directly to the target audience's goals, challenges, or responsibilities\n"
        "5. **Provides Forward-Looking Guidance**: Offers next steps, recommendations, or a vision of what comes next\n"
        "6. **Closes with Strength**: Ends on a confident, memorable note without introducing major new concepts\n\n"

        "## Conclusion Requirements\n\n"
        "### Core Elements\n"
        "- **Brief Recap**: 1–3 short paragraphs that recap the article's main themes and arguments\n"
        "- **Key Takeaways**: A concise list of the most important insights or principles readers should remember\n"
        "- **Implications**: A short discussion of what these insights mean for the reader's work, organization, or strategy\n"
        "- **Recommended Next Steps**: Practical suggestions for how readers can apply the article's ideas\n"
        "- **Closing Statement**: A strong closing paragraph that reinforces the key_message and value_proposition\n\n"

        "### Framing Guidelines\n"
        "- **Alignment**: Stay tightly aligned with the key_message and value_proposition from the overview\n"
        "- **No New Topics**: Do not introduce new major topics; focus on synthesis and reinforcement\n"
        "- **Clarity**: Use clear, direct language that makes the conclusions easy to act on\n"
        "- **Motivation**: Where appropriate, motivate the reader to take action or rethink their approach\n"
        "- **Brevity with Depth**: Keep the conclusion relatively concise while still offering meaningful insight\n\n"

        "### Writing Guidelines\n"
        "- **Tone and Style**: Follow the tone_and_style guidelines included in the filtered context\n"
        "- **Structure**: Use a clear heading for the conclusion (e.g., 'Conclusion' or 'Bringing It All Together')\n"
        "- **Lists**: Use bullet lists for key takeaways or next steps when it improves readability\n"
        "- **Transitions**: Ensure smooth transitions from recap → implications → next steps → closing\n"
        "- **Consistency**: Maintain consistency with the rest of the article's voice and level of formality\n\n"

        "## Target Audience and Context\n\n"
        "Ensure your conclusion speaks directly to the target audience implied by the overview and "
        "supports the article's differentiation_strategy where relevant. Reflect the audience's "
        "likely priorities and decision context.\n\n"

        "## Output Format\n\n"
        "Produce your conclusion as well-formatted markdown that includes:\n"
        "- A clear H2 or H3 heading for the conclusion section\n"
        "- Well-structured paragraphs with smooth flow\n"
        "- Bullet lists for key takeaways or recommended actions where appropriate\n"
        "- Professional formatting ready for integration into the final article\n\n"

        "Review the filtered article plan context carefully and write a conclusion that "
        "feels earned, clear, and actionable—one that reinforces the article's value while "
        "giving readers confidence about what to do next."
    )

    return instruction


conclusion_writer_agent = LlmAgent(
    name="conclusion_writer",
    model=gemini_model,
    description=(
        "Writes conclusion sections that synthesize key ideas, reinforce the core "
        "message and value proposition, and provide forward-looking guidance based "
        "on the article plan."
    ),
    instruction=_instruction_provider,  # Dynamic instruction provider
    output_key="conclusion_section",
    after_agent_callback=create_markdown_storage_callback("conclusion_section"),
)















