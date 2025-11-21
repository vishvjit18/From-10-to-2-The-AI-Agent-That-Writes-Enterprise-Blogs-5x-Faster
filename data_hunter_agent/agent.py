"""
DataHunter agent definition for the BlogResearch AI system.

This agent orchestrates research planning and data collection from SERP sources.
"""

from google.adk.agents import SequentialAgent

from .query_planner_agent import query_planner_agent
from .source_collector_agent import source_collector_agent


# Root agent orchestrates the full workflow: planning → collection
root_agent = SequentialAgent(
    name="data_hunter_agent",
    description=(
        "Master research agent that plans research queries and collects raw SERP/market data. "
        "Uses specialized sub-agents for query planning and source collection."
    ),
    sub_agents=[
        query_planner_agent,     # Step 1: Plan research tasks from user brief
        source_collector_agent,  # Step 2: Execute tasks and collect findings
    ],
)

__all__ = ["root_agent"]
