"""
GapAnalyzer agent definition.

This agent focuses on SERP analysis to uncover content gaps, complementary
to the DataHunter research workflows.

The agent uses a multi-agent architecture with specialized sub-agents:
- query_interpreter: Expands user queries into precise search strings
- serp_collector: Executes Google searches and collects SERP results
- root_agent: Synthesizes findings into gap analysis and opportunities
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import web_search
from utils.retry import gemini_model
from utils.storage import create_markdown_storage_callback
from .query_interpreter_agent import query_interpreter_agent


serp_tool_agent = LlmAgent(
    name="serp_tool_user",
    model=gemini_model,
    description=(
        "Executes Google searches and returns the raw results for structuring."
    ),
    instruction=(
       "You are a tool-using agent. Your purpose is to execute the research tasks "
        "and collect raw search results.\n\n"
        "Process:\n"
        "1. Read the research_plan {query_interpretation}.\n"
        "2. For each task, call the google_search tool with the exact search_query string.\n"
        "3. Collect all raw search results in a structured format.\n"
        "4. Return the complete set of raw results for structuring.\n\n"
        "Execute each search independently but collect all results together. "
    ),
    tools=[web_search],
    output_key="raw_serp_data",
)

# Synthesis agent that processes SERP results into gap analysis
synthesis_agent = LlmAgent(
    name="gap_synthesis",
    model=gemini_model,
    description=(
        "Synthesizes SERP results into gap analysis, themes, and "
        "differentiation opportunities."
    ),
    instruction=(
        "You are the Gap Synthesis Agent. Your task is to analyze the collected "
        "SERP results and synthesize them into actionable insights.\n\n"
        "You have access to:\n"
        "- SERP collection results: {raw_serp_data}\n\n"
        "Process:\n"
        "1. Review the SERP data collected by the sub-agents.\n"
        "2. Synthesize findings into three sections:\n"
        "   - SERP Themes: bullet list summarizing common angles, formats, "
        "     and buyer stages represented in the top results.\n"
        "   - Identified Gaps: bullet list calling out missing subtopics, "
        "     weak buyer-stage coverage, or depth deficits compared to "
        "     competitive content.\n"
        "   - Opportunities: concise recommendations (tone, assets, data) "
        "     that would differentiate new content from existing SERP results.\n"
        "3. If search results are insufficient, clearly note assumptions and "
        "   suggest follow-up research queries.\n\n"
        "Keep the tone analytical and reference source URLs when making "
        "specific claims. Base all insights on the actual SERP data provided."
    ),
    output_key="gap_analysis",
    after_agent_callback=create_markdown_storage_callback("gap_analysis"),  # Save output to local storage
)


# Root agent orchestrates the workflow using SequentialAgent pattern
root_agent = SequentialAgent(
    name="gap_analyzer_agent",
    description=(
        "Master research agent that plans research queries and collects raw SERP/market data. "
        "Uses specialized sub-agents for step 1: query planning, step 2: source collection, and step 3: gap analysis."
    ),
    sub_agents=[
        query_interpreter_agent,  # Step 1: Interpret query, expand to search strings
        serp_tool_agent,     # Step 2: Execute searches, collect SERP data
        synthesis_agent,          # Steps 3-4: Synthesize findings and identify gaps
    ],
)

