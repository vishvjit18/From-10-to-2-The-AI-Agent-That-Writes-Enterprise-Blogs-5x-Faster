"""
Query Planner sub-agent for DataHunter.

This agent handles Step 1: interpreting user research briefs and expanding them into
specific research tasks with search parameters.
"""

from google.adk.agents import LlmAgent

from . import ResearchPlan
from utils.storage import create_storage_callback


query_planner_agent = LlmAgent(
    name="query_planner",
    model="gemini-2.5-flash-lite",
    description=(
        "Interprets user research briefs and expands them into 1-4 specific research "
        "tasks with search parameters optimized for data collection."
    ),
    instruction=(
        "You are the Query Planner Agent. Your task is to analyze the user's research "
        "brief and break it down into 3 specific research tasks that will effectively "
        "gather the needed data.\n\n"
        "Process:\n"
        "1. Understand the core intent and scope of the user's research brief.\n"
        "3. The query should use the format '[topic] filetype:pdf site:.org'."
        # "2. Write query for each of these three type of sources: academic, industry, news.\n"
        "3. Create 3 research tasks, each with:\n"
        "   - search_query: A precise, effective search string\n"
        "   - source_pref: Source type\n"
        "   - freshness_window: Target recency (e.g., '≤18 months', '2024-2025')\n"
        "4. Ensure tasks are diverse enough to cover different angles while staying focused.\n\n"
        "Focus on queries that will yield actionable, current data for enterprise content "
        "creation.\n"
        "Prioritize recent academic papers."
        # "Prioritize recent statistics, academic papers, industry reports, and credible sources."
    ),
    output_schema=ResearchPlan,
    output_key="research_plan",
    after_agent_callback=create_storage_callback("research_plan"),  # Save output to local storage
)
