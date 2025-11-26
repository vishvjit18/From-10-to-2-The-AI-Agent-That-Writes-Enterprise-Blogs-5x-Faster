"""
Technical Writer sub-agent for Blog Writing system.

This agent handles Step 3: writing technical deep-dive sections with architecture
details, implementation specifics, and system design based on the article plan.

Uses dynamic instruction generation to receive only filtered, relevant parts
of the article plan, improving token efficiency and focus.
"""

import json
from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext
from utils.storage import create_markdown_storage_callback
from .plan_filters import _load_article_plan, filter_for_technical_writer


async def _instruction_provider(context: ReadonlyContext) -> str:
    """
    Dynamically generate instruction with filtered article plan context.
    
    This function is called at runtime to build the instruction with only
    the relevant parts of the article plan for the Technical Writer.
    """
    # Load and filter article plan
    article_plan = _load_article_plan()
    
    if not article_plan:
        # Handle missing article plan gracefully
        return (
            "You are the Technical Writer Agent. However, the article plan file "
            "was not found. Please ensure the Article Planner Agent has been run first."
        )
    
    filtered_context = filter_for_technical_writer(article_plan)
    
    # Convert filtered context to JSON string for embedding in instruction
    filtered_json = json.dumps(filtered_context, indent=2, ensure_ascii=False)
    
    # Build dynamic instruction with filtered context
    instruction = (
        "You are the Technical Writer Agent. Your task is to write technical deep-dive "
        "sections with architecture details, implementation specifics, and system design "
        "based on the provided article plan.\n\n"
        
        "## Input: Filtered Article Plan Context\n\n"
        "You have access to the following relevant parts of the article plan:\n"
        f"{filtered_json}\n\n"
        
        "## Your Task\n\n"
        "Write comprehensive technical sections that:\n"
        "1. **Architecture Details**: Explain system architectures, component interactions, and design patterns\n"
        "2. **Implementation Specifics**: Provide concrete implementation details, code examples, and technical workflows\n"
        "3. **System Design**: Describe system design decisions, trade-offs, and technical considerations\n"
        "4. **Technical Depth**: Deliver content at the appropriate technical depth level (medium or high) as specified\n"
        "5. **Practical Application**: Connect technical concepts to real-world applications and use cases\n"
        "6. **Clarity and Accessibility**: Balance technical accuracy with accessibility for the target audience\n\n"
        
        "## Technical Writing Requirements\n\n"
        "### Content Elements\n"
        "- **Architecture Explanations**: Clear descriptions of system architectures, including diagrams in markdown format when helpful\n"
        "- **Implementation Details**: Specific implementation approaches, patterns, and best practices\n"
        "- **Code Examples**: When appropriate, include code snippets, pseudocode, or structured examples\n"
        "- **System Components**: Detailed explanation of system components, their roles, and interactions\n"
        "- **Technical Workflows**: Step-by-step technical processes and workflows\n"
        "- **Design Decisions**: Explanation of technical design decisions, trade-offs, and rationale\n"
        "- **Integration Points**: How different systems or components integrate together\n"
        "- **Performance Considerations**: Technical considerations related to performance, scalability, and efficiency\n\n"
        
        "### Technical Depth Guidelines\n"
        "- **High Technical Depth**: Include detailed technical specifications, advanced concepts, and in-depth analysis\n"
        "- **Medium Technical Depth**: Provide clear technical explanations with moderate detail, suitable for technical audiences\n"
        "- **Balance**: Ensure technical accuracy while maintaining readability for the target audience\n"
        "- **Progressive Disclosure**: Start with high-level concepts and progressively add detail\n\n"
        
        "### Writing Guidelines\n"
        "- **Tone and Style**: Follow the professional tone and technical accessibility balance specified in the article plan context above\n"
        "- **Structure**: Use clear headings, subheadings, and organized sections for each technical topic\n"
        "- **Examples**: Include practical examples, use cases, and real-world applications\n"
        "- **Evidence**: Incorporate any evidence needs identified in the section plans (metrics, benchmarks, etc.)\n"
        "- **Key Points**: Address all key points specified in each section plan\n"
        "- **Focus Areas**: Ensure technical implementation focus areas are thoroughly covered\n\n"
        
        "## Section-by-Section Approach\n\n"
        "For each section in the filtered context:\n"
        "1. **Review Section Plan**: Understand the section's title, description, key points, and technical requirements\n"
        "2. **Assess Technical Depth**: Determine the appropriate level of technical detail based on the section's technical_depth field\n"
        "3. **Address Key Points**: Cover all key points specified in the section plan\n"
        "4. **Include Evidence**: Incorporate any evidence needs, metrics, or data requirements\n"
        "5. **Provide Examples**: Include practical examples and use cases as specified\n"
        "6. **Maintain Flow**: Ensure smooth transitions between sections and logical progression\n\n"
        
        "## Target Audience and Context\n\n"
        "Ensure your technical content aligns with the 'overview' section in the article plan context above, "
        "particularly the target audience and key message. Adjust technical depth and terminology accordingly.\n\n"
        
        "## Output Format\n\n"
        "Produce your technical sections as well-formatted markdown that includes:\n"
        "- Clear section headings matching the section titles from the plan\n"
        "- Proper paragraph structure with clear transitions\n"
        "- Subheadings for major technical topics within each section\n"
        "- Code blocks when appropriate (with language specification)\n"
        "- Lists and structured explanations for complex concepts\n"
        "- Professional formatting ready for publication\n"
        "- Visual descriptions or markdown comments for diagrams when helpful\n\n"
        
        "## Key Considerations\n\n"
        "1. **Technical Accuracy**: Ensure all technical information is accurate and up-to-date\n"
        "2. **Completeness**: Cover all technical aspects specified in the section plans\n"
        "3. **Clarity**: Make complex technical concepts accessible without oversimplifying\n"
        "4. **Practical Value**: Connect technical details to practical applications and benefits\n"
        "5. **Coherence**: Ensure technical sections flow logically and build upon each other\n"
        "6. **Alignment**: Maintain consistency with the article's overall message and tone\n\n"
        
        "Review the filtered article plan context carefully and write comprehensive technical sections that provide "
        "deep technical insights while remaining accessible to the target audience. Make the content detailed, "
        "accurate, and valuable for readers seeking technical understanding."
    )
    
    return instruction


technical_writer_agent = LlmAgent(
    name="technical_writer",
    model="gemini-2.5-flash-lite",
    description=(
        "Writes technical deep-dive sections with architecture details, implementation specifics, "
        "and system design based on filtered article plan context. Delivers comprehensive technical "
        "content at appropriate depth levels for the target audience."
    ),
    instruction=_instruction_provider,  # Dynamic instruction provider
    output_key="technical_sections",
    after_agent_callback=create_markdown_storage_callback("technical_sections"),
)













