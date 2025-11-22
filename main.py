"""
Main entry point for DataHunter agent package.

This module handles initialization and configuration for the DataHunter agents.
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from data_hunter_agent.query_planner_agent import query_planner_agent

# Load environment variables from .env file
load_dotenv()

# Set up Google API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize runner for query planner agent
enhanced_runner = InMemoryRunner(agent=query_planner_agent, app_name="data_hunter_agent")


async def test_query_planner_agent():
    """Test the query planner agent with a sample research brief."""
    response = await enhanced_runner.run_debug(
        "I want to research the latest trends in AI and machine learning."
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(test_query_planner_agent())
