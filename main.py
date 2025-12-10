"""
Utility entry point for running sample agents in the blog writing system.

This module handles initialization and configuration for quick local testing.
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from blog_writing_agent.final_formatter_agent import final_formatter_agent
from utils.config import config
# Load environment variables from .env file
load_dotenv()

# Set up Google API key from environment
# Set up Google API key from config

GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize runner for query planner agent
enhanced_runner = InMemoryRunner(agent=final_formatter_agent, app_name="blog_writing_agent")


async def test_query_planner_agent():
    """Test the query planner agent with a sample research brief."""
    response = await enhanced_runner.run_debug(
        "Ai agents in creative writing"
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(test_query_planner_agent())
