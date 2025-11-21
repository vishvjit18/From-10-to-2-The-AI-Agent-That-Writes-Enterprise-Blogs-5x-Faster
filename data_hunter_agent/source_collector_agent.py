"""
Source Collector sub-agent for DataHunter.

This agent handles Step 2: executing research tasks and collecting findings from SERP sources.
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search

from . import ResearchFinding, ResearchBatch


# Tool-using agent that executes search tasks
tool_collector_agent = LlmAgent(
    name="tool_collector",
    model="gemini-2.5-flash-lite",
    description=(
        "Executes research tasks by calling search tools and collecting raw results."
    ),
    instruction=(
        "You are a tool-using agent. Your purpose is to execute the research tasks "
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


# Structuring agent that normalizes results into ResearchFinding records
structuring_agent = LlmAgent(
    name="result_structuring",
    model="gemini-2.5-flash-lite",
    description=(
        "Takes raw search results and structures them into standardized ResearchFinding records."
    ),
    instruction=(
        "You are the Result Structuring Agent. Your task is to take the raw search "
        "results and convert them into standardized ResearchFinding records.\n\n"
        "Process:\n"
        "1. Read the raw_search_results and research_plan from previous steps.\n"
        "2. For each search result, create a ResearchFinding with:\n"
        "   - title: The result title\n"
        "   - snippet: The description/snippet text\n"
        "   - url: The source URL\n"
        "   - source_type: Inferred type ('academic', 'industry', 'news', 'blog', 'other')\n"
        "   - credibility_guess: Initial assessment ('high', 'medium', 'low') based on domain\n"
        "   - tags: Relevant categorization tags\n"
        "   - task_id: Index of the research task that produced this result\n"
        "3. Aggregate all findings into a ResearchBatch.\n"
        "4. Calculate total_findings and tasks_executed counts.\n\n"
        "Base credibility assessments on recognizable domains (e.g., .edu = high, "
        ".com commercial sites = medium, unknown = low). Include relevant tags like "
        "'statistics', '2024', 'report', etc."
    ),
    output_schema=ResearchBatch,
    output_key="collected_findings",
)


# Main collector agent combining tool usage and structuring
source_collector_agent = SequentialAgent(
    name="source_collector",
    description=(
        "A two-step agent that first executes `tool_collector_agent` using tools, "
        "then structures the results into standardized findings using `structuring_agent`."
    ),
    sub_agents=[tool_collector_agent, structuring_agent],
)
