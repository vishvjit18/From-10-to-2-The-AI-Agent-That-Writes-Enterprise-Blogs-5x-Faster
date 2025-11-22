"""
DataHunter agent definition for the BlogResearch AI system.

This agent orchestrates research planning and data collection from SERP sources.
"""
from .query_planner_agent import query_planner_agent
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search
from utils.storage import create_markdown_storage_callback

# Tool-using agent that executes search tasks
tool_collector_agent = LlmAgent(
    name="tool_collector",
    model="gemini-2.5-flash-lite",
    description=(
        "Executes research tasks by calling search tools and collecting raw results."
    ),
    instruction=(
        "You are a tool-using agent. Your purpose is to execute the research tasks "
        "and collect raw search results.\n\n"
        "Process:\n"
        "1. Read the research_plan {research_plan}.\n"
        "2. For each task, call the google_search tool with the exact search_query string.\n"
        "3. Collect all raw search results in a structured format.\n"
        "4. Return the complete set of raw results for structuring.\n\n"
        "Execute each search independently but collect all results together. "
        # "Note that future implementations may use different tools based on source_pref "
        # "(e.g., MCP servers for academic databases)."
    ),
    tools=[google_search],
    output_key="raw_search_results",
)


# Synthesis agent that processes SERP results into gap analysis
synthesis_agent = LlmAgent(
    name="gap_synthesis",
    model="gemini-2.5-flash-lite",
    description=(
        "Synthesizes SERP results into gap analysis, themes, and "
        "differentiation opportunities."
    ),
    instruction=(
        "You are the Gap Synthesis Agent. Your task is to analyze the collected "
        "SERP results and synthesize them into actionable insights.\n\n"
        "You have access to:\n"
        "- SERP collection results: {raw_search_results}\n\n"
        "Process:\n"
        "1. Review the SERP data collected.\n"
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
    output_key="data_analysis",
    after_agent_callback=create_markdown_storage_callback("data_analysis"),  # Save output to local storage
)

# Root agent orchestrates the full workflow: planning → collection
root_agent = SequentialAgent(
    name="data_hunter_agent",
    description=(
        "Master research agent that plans research queries and collects raw SERP/market data. "
        "Uses specialized sub-agents for query planning and source collection."
    ),
    sub_agents=[
        query_planner_agent,     # Step 1: Plan research tasks from user brief
        tool_collector_agent,  # Step 2: Execute tasks and collect findings
        synthesis_agent,  # Step 3: Synthesize findings into gap analysis
    ],
)

__all__ = ["root_agent"]
