"""
Final Formatter sub-agent for Blog Writing system.

This agent handles final formatting: combining introduction and technical sections
into a publication-ready blog article with optimized structure and professional formatting.

Takes input from Introduction Writer Agent and Technical Writer Agent outputs.
"""

import re
from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext
from utils.storage import create_markdown_storage_callback


def _load_content_files() -> tuple[str, str]:
    """Load the introduction and technical sections from markdown files."""
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
    technical_content = _load_markdown_file(
        data_dir / "technical_sections.md",
        "[Technical sections file not found. Please run the Technical Writer Agent first.]"
    )
    
    return introduction_content, technical_content


async def _instruction_provider(context: ReadonlyContext) -> str:
    """
    Dynamically generate instruction with loaded content from markdown files.
    
    This function is called at runtime to build the instruction with the actual
    content from the introduction and technical section files.
    """
    # Load content from files
    introduction_content, technical_content = _load_content_files()
    
    # Build dynamic instruction with loaded content
    instruction = (
        "You are the Final Formatter Agent. Your task is to combine the introduction and "
        "technical sections into a publication-ready blog article with professional formatting.\n\n"
        
        "## Input: Content Sections\n\n"
        "You have access to the following content sections:\n\n"
        
        "### Introduction Section\n"
        f"{introduction_content}\n\n"
        
        "### Technical Sections\n"
        f"{technical_content}\n\n"
        
        "## Your Task\n\n"
        "Combine and format these sections into a complete, publication-ready blog article that:\n"
        "1. **Seamless Integration**: Creates smooth transitions between the introduction and technical sections\n"
        "2. **Structure Optimization**: Ensures logical flow and clear hierarchy of headings\n"
        "3. **Professional Formatting**: Applies consistent markdown formatting throughout\n"
        "4. **Readability**: Optimizes formatting for maximum readability and engagement\n"
        "5. **Completeness**: Produces a cohesive, complete article ready for publication\n\n"
        
        "## Formatting Requirements\n\n"
        "### Markdown Structure\n"
        "- Use proper heading hierarchy (H1 for title, H2 for main sections, H3 for subsections)\n"
        "- Ensure consistent heading styles and capitalization\n"
        "- Use proper spacing between sections (blank lines between paragraphs and sections)\n"
        "- Format lists, code blocks, and other markdown elements consistently\n"
        "- Ensure all markdown syntax is valid and properly formatted\n\n"
        
        "### Content Organization\n"
        "- Start with the introduction section as the opening of the article\n"
        "- Follow with the technical sections in logical order\n"
        "- Create smooth transitions between sections where needed\n"
        "- Ensure the article flows naturally from introduction to technical content\n"
        "- Maintain consistent tone and style throughout\n\n"
        
        "### Professional Presentation\n"
        "- Remove any redundant headings or duplicate content\n"
        "- Ensure consistent formatting of code blocks, lists, and emphasis\n"
        "- Optimize paragraph length for readability\n"
        "- Use appropriate markdown elements (bold, italic, links) consistently\n"
        "- Ensure the article looks polished and professional\n\n"
        
        "### Quality Checks\n"
        "- Verify all sections are included and properly formatted\n"
        "- Check that headings are properly nested and consistent\n"
        "- Ensure no formatting artifacts or inconsistencies\n"
        "- Verify the article reads as a cohesive whole\n"
        "- Make sure the final output is ready for immediate publication\n\n"
        
        "## Output Format\n\n"
        "Produce a complete, well-formatted markdown article that:\n"
        "- Has a clear title (H1 heading)\n"
        "- Includes the introduction section seamlessly\n"
        "- Integrates all technical sections with proper formatting\n"
        "- Uses consistent markdown syntax throughout\n"
        "- Is ready for publication without further editing\n\n"
        
        "## Key Considerations\n\n"
        "1. **Preserve Content**: Keep all important content from both input sections\n"
        "2. **Enhance Flow**: Add transitions or minor edits only to improve readability\n"
        "3. **Consistency**: Ensure formatting is consistent throughout the entire article\n"
        "4. **Completeness**: The final article should feel complete and cohesive\n"
        "5. **Professional Quality**: The output should meet publication standards\n\n"
        
        "Combine the introduction and technical sections into a single, publication-ready blog article. "
        "Focus on creating a seamless, well-formatted, professional document that is ready for immediate use."
    )
    
    return instruction


final_formatter_agent = LlmAgent(
    name="final_formatter",
    model="gemini-2.5-flash-lite",
    description=(
        "Combines introduction and technical sections into a publication-ready blog article "
        "with optimized markdown formatting, structure, and professional presentation."
    ),
    instruction=_instruction_provider,  # Dynamic instruction provider
    output_key="blog_article",
    after_agent_callback=create_markdown_storage_callback("blog_article"),
)

