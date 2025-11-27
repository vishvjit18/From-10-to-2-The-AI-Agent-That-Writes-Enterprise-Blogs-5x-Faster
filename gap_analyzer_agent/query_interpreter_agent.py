"""
Query Interpreter sub-agent for GapAnalyzer.

This agent handles Step 1: interpreting user queries and expanding them into
precise search strings for SERP analysis.
"""

from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent
from utils.retry import gemini_model
from utils.storage import create_storage_callback


class QueryInterpretationOutput(BaseModel):
    """Output schema for query interpretation results."""

    original_query: str = Field(
        description="The original user query or keyword as provided."
    )
    search_strings: list[str] = Field(
        description=(
            "List of 1-2 precise search strings optimized for competitive "
            "SERP analysis. Each string should be concise but comprehensive."
        ),
        min_length=1,
        max_length=2,
    )
    rationale: str = Field(
        description=(
            "Brief explanation of why these specific search strings were chosen, "
            "including any expansion or refinement decisions."
        )
    )

query_interpreter_agent = LlmAgent(
    name="query_interpreter",
    model=gemini_model,
    description=(
        "Interprets user queries and expands them into 1-2 precise search "
        "strings optimized for competitive SERP analysis."
    ),
    instruction=(
        "You are the Query Interpreter Agent. Your task is to analyze the "
        "user's keyword or topic query and expand it into precise 3 search strings "
        "for competitive landscape analysis.\n\n"
        "Process:\n"
        "1. Understand the core intent and context of the user's query.\n"
        "2. Identify if the query needs expansion or refinement for effective "
        "SERP research.\n"
        "3.The query should use the format '[topic] filetype:pdf related:.edu'.\n"
        "4. Provide a brief rationale explaining your search string choices.\n\n"
        "Keep search strings concise but comprehensive enough to capture "
        "competitive content."
    ),
    output_schema=QueryInterpretationOutput,
    output_key="query_interpretation",
    after_agent_callback=create_storage_callback("query_interpretation"),
)

