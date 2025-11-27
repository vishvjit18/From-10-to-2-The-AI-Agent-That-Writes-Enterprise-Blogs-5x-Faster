"""
Article Planner sub-agent for Blog Writing system.

This agent handles Step 1: analyzing research and gap analysis files to create
a comprehensive, structured article plan with sections, key points, and content requirements.
"""
import json
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext
from utils.retry import gemini_model
from utils.storage import create_storage_callback
from . import ArticlePlan


def _load_analysis_files() -> tuple[str, str]:
    """Load the analysis files from data/collections directory."""
    def _load_file(file_path: Path, error_message: str) -> str:
        """Helper function to load and parse a JSON file."""
        if not file_path.exists():
            return error_message
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                plan_data = data.get("output", data)
                return json.dumps(plan_data, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"[Error loading {file_path.name}: {e}]"
    
    data_dir = Path("data/collections")
    data_analysis = _load_file(
        data_dir / "data_analysis.md",
        "[Data analysis file not found. Please run the Data Hunter Agent first.]"
    )
    gap_analysis = _load_file(
        data_dir / "gap_analysis.md",
        "[Gap analysis file not found. Please run the Gap Analysis Agent first.]"
    )
    
    return data_analysis, gap_analysis



data_analysis, gap_analysis = _load_analysis_files()
root_agent = LlmAgent(
    name="article_planner",
    model=gemini_model,
    description=(
        "Analyzes research and gap analysis files to create a comprehensive, structured "
        "article plan with sections, key points, evidence needs, and content requirements."
    ),
    instruction = (
        "You are the Article Planner Agent. Your task is to analyze the provided analysis "
        "files and create a detailed, structured plan for a comprehensive blog article.\n\n"
        
        "## Analysis Files\n\n"
        "You have access to two analysis files:\n"
        f"- Data Analysis File:\n{data_analysis}\n\n"
        f"- Gap Analysis File:\n{gap_analysis}\n\n"
        
        "## Your Task\n\n"
        "Analyze both files to understand:\n"
        "- Key themes and patterns identified in the research\n"
        "- Content gaps and opportunities for differentiation\n"
        "- Required focus areas and topics to address\n"
        "- Evidence and data needs\n"
        "- Visual opportunities\n\n"
        
        "## Output: Structured Article Plan\n\n"
        "Create a comprehensive article plan in JSON format that includes:\n\n"
        
        "### 1. Article Overview (overview field)\n"
        "Provide a dictionary with:\n"
        "- target_audience: Description of the target audience\n"
        "- purpose: Main purpose of the article\n"
        "- key_message: Core message to convey\n"
        "- value_proposition: Value proposition for readers\n"
        "- differentiation_strategy: Strategy based on identified gaps\n\n"
        
        "### 2. Article Structure (structure field)\n"
        "Provide a list of section plans, each with:\n"
        "- title: Section title\n"
        "- description: Brief description of what this section covers\n"
        "- estimated_word_count: Estimated word count for this section\n"
        "- key_points: List of key points to cover\n"
        "- evidence_needs: List of required evidence, statistics, or data\n"
        "- technical_depth: Required technical depth level ('high', 'medium', 'low', 'none')\n"
        "- practical_examples: List of types of practical examples needed\n"
        "- conceptual_distinctions: List of conceptual distinctions to make\n"
        "- focus_areas: List of focus areas this section addresses\n\n"
        
        "### 3. Focus Areas Mapping (focus_areas_mapping field)\n"
        "Provide an object with the following fields, each containing a list of section titles:\n"
        "- technical_implementation: List of section titles that address technical implementation\n"
        "- evidence_and_metrics: List of section titles that cover evidence and metrics\n"
        "- conceptual_distinctions: List of section titles that explore conceptual distinctions\n"
        "- ethical_considerations: List of section titles that address ethical considerations\n\n"
        
        "### 4. Visual Opportunities (visual_opportunities field)\n"
        "Provide a list of visual opportunities, each with:\n"
        "- type: Type of visual ('infographic', 'diagram', 'process_flow', 'data_visualization')\n"
        "- description: Description of the visual element\n"
        "- suggested_location: Where in the article this visual should appear\n"
        "- purpose: Purpose of this visual element\n\n"
        
        "### 5. Tone and Style Guidelines (tone_and_style field)\n"
        "Provide an object with the following fields:\n"
        "- professional_tone: Professional tone requirements\n"
        "- technical_accessibility_balance: Balance between technical depth and accessibility\n"
        "- critical_thinking: Critical thinking and balanced perspective needs\n"
        "- evidence_based_approach: Evidence-based approach requirements\n\n"
        
        "## Planning Principles\n\n"
        "1. **Address Gaps**: Ensure the plan addresses all identified content gaps\n"
        "2. **Leverage Opportunities**: Incorporate differentiation opportunities from analysis\n"
        "3. **Evidence-Based**: Plan for data, metrics, and concrete examples throughout\n"
        "4. **Structured Flow**: Create logical progression from concepts to applications\n"
        "5. **Comprehensive Coverage**: Ensure all focus areas are adequately covered\n"
        "6. **Actionable Content**: Plan for practical, actionable insights\n\n"
        
        "## Output Format\n\n"
        "Produce your plan as a structured JSON object matching the ArticlePlan schema:\n"
        "- Use the exact field names specified above\n"
        "- Ensure all required fields are present\n"
        "- Provide specific, actionable guidance for content writers\n"
        "- Make the plan comprehensive and detailed\n\n"
        
        "Begin analyzing the files and creating the comprehensive article plan now."
    ),
    output_schema=ArticlePlan,
    output_key="article_plan",
    after_agent_callback=create_storage_callback("article_plan"),
)

