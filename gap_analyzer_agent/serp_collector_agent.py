"""
SERP Collector sub-agent for GapAnalyzer.

This agent handles Step 2: executing Google searches and collecting SERP results
for analysis.
"""

from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search


class SERPResultItem(BaseModel):
    """Individual SERP result item."""

    title: str = Field(description="The title of the search result.")
    snippet: str = Field(
        description="The snippet or description text from the search result."
    )
    url: str = Field(description="The URL of the search result.")
    focus_area: str = Field(
        description="Inferred focus area or topic based on title and snippet."
    )


class SERPCollectionOutput(BaseModel):
    """Output schema for SERP collection results."""

    total_results: int = Field(
        description="Total number of SERP results collected across all searches.",
        ge=0,
    )
    results: list[SERPResultItem] = Field(
        description="List of all collected SERP results with titles, snippets, URLs, and focus areas."
    )
    themes: list[str] = Field(
        description="Key themes observed from analyzing titles and snippets across all results."
    )
    patterns: str = Field(
        description=(
            "Notable patterns observed in content format, buyer stage coverage, "
            "or other competitive insights. If results are sparse, note this explicitly."
        )
    )


serp_tool_agent = LlmAgent(
    name="serp_tool_user",
    model="gemini-2.5-flash-lite",
    description=(
        "Executes Google searches and returns the raw results for structuring."
    ),
    instruction=(
        "You are a tool-using agent. Your only purpose is to execute the `google_search` tool and return its raw, unmodified output.\n\n"
        "- Read the search strings provided in the `{query_interpretation}` input.\n"
        "- Call the `google_search` tool for each of those strings.\n"
        "- Return the direct, raw JSON output from the `google_search` tool like this: \n"
        '```json\n'
        '[\n'
        '  {\n'
        '    "title": "Example Title 1",\n'
        '    "url": "https://example.com/page1",\n'
        '    "snippet": "This is a snippet for the first example search result..."\n'
        '  },\n'
        '  {\n'
        '    "title": "Example Title 2",\n'
        '    "url": "https://example.com/page2",\n'
        '    "snippet": "This is a snippet for the second example search result..."\n'
        '  }\n'
        ']\n'
        '```'
    ),
    tools=[google_search],
    output_key="raw_serp_data",
)


serp_structuring_agent = LlmAgent(
    name="serp_structuring_agent",
    model="gemini-2.5-flash-lite",
    description=(
        "Takes raw SERP data and structures it into a JSON format."
    ),
    instruction=(
        "You are the SERP Structuring Agent. Your task is to take the raw "
        "search results and structure them into the required format.\n\n"
        "Process:\n"
        "1. Read the raw search results stored in {raw_serp_data}.\n"
        "2. Extract and organize the following from each result:\n"
        "   - Title, Snippet/description, URL\n"
        "   - An inferred focus area (based on title/snippet)\n"
        "3. Compile all results into the final structured summary, identifying key "
        "   themes and patterns observed across the results.\n\n"
        "If search results are sparse or insufficient, note this "
        "explicitly in the patterns field."
    ),
    output_schema=SERPCollectionOutput,
    output_key="serp_results",
)


serp_collector_agent = SequentialAgent(
    name="serp_collector",
    description=(
        "A two-step agent that first collects SERP results using a tool and "
        "then structures the output into a consistent JSON format."
    ),
    sub_agents=[serp_tool_agent, serp_structuring_agent],
)

