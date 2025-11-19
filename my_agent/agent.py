"""
DataHunter agent definition for the BlogResearch AI system.

This version intentionally runs without any external tools, leaning entirely on
Gemini's reasoning to plan and summarize research workflows.
"""

from google.adk.agents import Agent
from google.adk.tools import google_search


root_agent = Agent(
    name="data_hunter_agent",
    model="gemini-2.5-flash-lite",
    description=(
        """ Master research agent that uses Google Search to find and synthesize
         information for enterprise content. """
    ),
    instruction=(
        """You are the DataHunter, an AI research specialist. Your mission is to
        use the `google_search` tool to execute the user's research query.
        Follow these steps:
        1. Analyze Query: Understand the core intent of the user's request.
        2. Execute Search: Use the `google_search` tool with a precise and
            effective query string to find relevant information.
        3. Synthesize & Deliver: Summarize the findings from the search
            results into a coherent, bulleted list. Provide the source URLs
            for each finding. Present the information clearly in markdown format."""
    ),
    tools=[google_search],
)
