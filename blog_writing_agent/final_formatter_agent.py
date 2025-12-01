"""
Final Formatter sub-agent for Blog Writing system.

This agent handles final formatting: intelligently weaving together introduction, 
evidence-based content, conceptual explanations, technical sections, and conclusion
into a cohesive, publication-ready blog article with enterprise-grade formatting.

Takes input from all specialized writer agents:
- Introduction Writer Agent
- Evidence Writer Agent  
- Conceptual Writer Agent
- Technical Writer Agent
- Conclusion Writer Agent
"""

import re
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext
from utils.retry import gemini_model
from utils.storage import create_markdown_storage_callback


def _load_content_files() -> tuple[str, str, str, str, str]:
    """Load all blog section files from markdown."""
    def _load_markdown_file(file_path: Path, error_message: str) -> str:
        """Helper function to load a markdown file and strip YAML frontmatter."""
        if not file_path.exists():
            return error_message
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove YAML frontmatter (between --- markers)
            # Pattern matches: ---\n...content...\n---
            frontmatter_pattern = r'^---\s*\n.*?\n---\s*\n'
            content_without_frontmatter = re.sub(frontmatter_pattern, '', content, flags=re.DOTALL)
            
            # Clean up any leading/trailing whitespace
            return content_without_frontmatter.strip()
        except Exception as e:
            return f"[Error loading {file_path.name}: {e}]"
    
    data_dir = Path("data/collections")
    
    introduction_content = _load_markdown_file(
        data_dir / "introduction_section.md",
        "[Introduction section file not found. Please run the Introduction Writer Agent first.]"
    )
    evidence_content = _load_markdown_file(
        data_dir / "evidence_sections.md",
        "[Evidence sections file not found. Please run the Evidence Writer Agent first.]"
    )
    conceptual_content = _load_markdown_file(
        data_dir / "conceptual_sections.md",
        "[Conceptual sections file not found. Please run the Conceptual Writer Agent first.]"
    )
    technical_content = _load_markdown_file(
        data_dir / "technical_sections.md",
        "[Technical sections file not found. Please run the Technical Writer Agent first.]"
    )
    conclusion_content = _load_markdown_file(
        data_dir / "conclusion_section.md",
        "[Conclusion section file not found. Please run the Conclusion Writer Agent first.]"
    )
    
    return introduction_content, evidence_content, conceptual_content, technical_content, conclusion_content


async def _instruction_provider(context: ReadonlyContext) -> str:
    """
    Dynamically generate instruction with loaded content from markdown files.
    
    This function is called at runtime to build the instruction with the actual
    content from all blog section files.
    """
    # Load content from files
    introduction_content, evidence_content, conceptual_content, technical_content, conclusion_content = _load_content_files()
    
    # Build dynamic instruction with loaded content
    instruction = (
        "You are the Final Formatter Agent. Your task is to weave together multiple specialized "
        "content sections into a cohesive, publication-ready blog article with professional formatting "
        "and engaging narrative flow.\n\n"
        
        "## Input: Content Sections\n\n"
        "You have access to the following specialized content sections:\n\n"
        
        "### 1. Introduction Section\n"
        f"{introduction_content}\n\n"
        
        "### 2. Evidence-Based Content\n"
        "This section contains data-driven insights, research summaries, metrics, case studies, "
        "and concrete examples:\n"
        f"{evidence_content}\n\n"
        
        "### 3. Conceptual Explanations\n"
        "This section provides frameworks, definitions, distinctions, and high-level concepts "
        "to build reader understanding:\n"
        f"{conceptual_content}\n\n"
        
        "### 4. Technical Deep-Dive Sections\n"
        f"{technical_content}\n\n"
        
        "### 5. Conclusion Section\n"
        f"{conclusion_content}\n\n"
        
        "## Your Task\n\n"
        "Masterfully integrate these diverse sections into a unified, publication-ready blog article that:\n\n"
        
        "1. **Strategic Content Synthesis**: Intelligently merge evidence-based data, conceptual frameworks, "
        "and technical details to create a compelling narrative\n"
        "2. **Balanced Information Architecture**: Blend statistics, case studies, definitions, and technical "
        "content proportionally to maintain reader engagement\n"
        "3. **Seamless Transitions**: Create natural bridges between data-heavy sections, conceptual "
        "explanations, and technical details\n"
        "4. **Hierarchical Structure**: Organize content logically with proper heading levels and subsection flow\n"
        "5. **Professional Polish**: Apply enterprise-grade formatting for immediate publication\n\n"
        
        "## Content Integration Strategy\n\n"
        
        "### Optimal Section Arrangement\n"
        "For each major topic area, intelligently interweave:\n"
        "- **Conceptual explanations** to establish understanding\n"
        "- **Evidence and data** to substantiate claims\n"
        "- **Technical details** to provide actionable depth\n"
        "- **Case studies/examples** to illustrate real-world application\n\n"
        
        "### Avoid These Common Pitfalls\n"
        "- Don't group all data/metrics in one section; distribute throughout where relevant\n"
        "- Don't separate conceptual definitions from their application context\n"
        "- Don't create jarring shifts between abstract concepts and concrete examples\n"
        "- Don't duplicate content—synthesize overlapping information intelligently\n\n"
        
        "## Formatting Requirements\n\n"
        
        "### Markdown Structure Excellence\n"
        "- **H1**: Single article title only\n"
        "- **H2**: Major section headings (5-7 main sections recommended)\n"
        "- **H3**: Subsections within major sections\n"
        "- **H4**: Use sparingly for detailed breakdowns if needed\n"
        "- Ensure consistent capitalization (Title Case for H2, Sentence case for H3)\n"
        "- Use proper spacing: blank lines between all paragraphs and sections\n\n"
        
        "### Content Element Formatting\n"
        "- **Data/Metrics**: Format consistently (bold for key numbers, use tables where appropriate)\n"
        "- **Case Studies**: Use clear demarcation (bold headings, structured format)\n"
        "- **Lists**: Use bullet points for features/benefits, numbered lists for processes/steps\n"
        "- **Definitions**: Use bold or italic consistently for terms being defined\n"
        "- **Emphasis**: Use **bold** for critical takeaways, *italic* for subtle emphasis\n"
        "- **Links**: Ensure all URLs are properly formatted (if present)\n\n"
        
        "### Enterprise-Grade Presentation\n"
        "- Remove redundant headings and consolidate duplicate information\n"
        "- Optimize paragraph length: 3-5 sentences for web readability\n"
        "- Ensure smooth narrative flow between evidence, concepts, and technical details\n"
        "- Maintain professional, authoritative tone throughout\n"
        "- Polish transitions to feel natural, not forced\n\n"
        
        "## Quality Assurance Checklist\n\n"
        "Before finalizing, verify:\n"
        "- ✓ All five input sections are represented and integrated\n"
        "- ✓ Data and evidence support claims throughout (not isolated)\n"
        "- ✓ Conceptual frameworks are explained before being applied\n"
        "- ✓ Technical content is accessible yet detailed\n"
        "- ✓ Conclusion ties together key themes from all sections\n"
        "- ✓ Heading hierarchy is logical and consistent\n"
        "- ✓ No formatting artifacts or markdown syntax errors\n"
        "- ✓ Article reads as a unified piece, not disparate sections\n"
        "- ✓ Ready for immediate publication without further editing\n\n"
        
        "## Output Structure Template\n\n"
        "Your final article should follow this proven structure:\n\n"
        "```\n"
        "# [Compelling Title]\n\n"
        "[Introduction - sets context and hooks reader]\n\n"
        "## [Section 1 - Core Topic/Problem]\n"
        "[Blend: concept definition → evidence → examples]\n\n"
        "## [Section 2 - Deep Dive/Solution]\n"
        "[Blend: framework → data/metrics → technical details]\n\n"
        "## [Section 3-5 - Supporting Sections]\n"
        "[Continue strategic integration of all content types]\n\n"
        "## [Final Section - Practical Application/Next Steps]\n"
        "[Actionable guidance with supporting evidence]\n\n"
        "## Conclusion\n"
        "[Synthesized takeaways and forward-looking perspective]\n"
        "```\n\n"
        
        "## Key Principles\n\n"
        "1. **Content Fidelity**: Preserve all substantive information from input sections\n"
        "2. **Strategic Synthesis**: Don't just concatenate—intelligently merge related content\n"
        "3. **Reader-Centric Flow**: Prioritize logical progression and engagement over rigid section boundaries\n"
        "4. **Enterprise Quality**: Match the polish and professionalism of top-tier business publications\n"
        "5. **Immediate Usability**: Deliver a truly publication-ready asset\n\n"
        
        "Transform these specialized sections into a cohesive, compelling, and professionally formatted "
        "blog article that seamlessly integrates evidence, concepts, technical depth, and practical guidance. "
        "The final output should read as a unified narrative crafted by a single expert author, not as "
        "assembled sections from multiple sources."
    )
    
    return instruction

final_formatter_agent = LlmAgent(
    name="final_formatter",
    model=gemini_model,
    description=(
        "Synthesizes multiple specialized content sections (introduction, evidence, conceptual "
        "explanations, technical details, and conclusion) into a unified, publication-ready "
        "blog article with enterprise-grade formatting, strategic content integration, and "
        "professional narrative flow. Ensures seamless blending of data, concepts, and technical "
        "depth for maximum reader engagement and immediate publication readiness."
    ),
    instruction=_instruction_provider,  # Dynamic instruction provider
    output_key="blog_article",
    after_agent_callback=create_markdown_storage_callback("blog_article"),
)

