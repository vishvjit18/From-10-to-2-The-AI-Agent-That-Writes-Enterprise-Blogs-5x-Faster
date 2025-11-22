"""DataHunter Agent package for gathering raw SERP and market data."""

from pydantic import BaseModel, Field
from typing import List, Optional


class ResearchTask(BaseModel):
    """A single research task with specific parameters."""

    search_query: str = Field(
        description="The exact search query to execute for this research task."
    )
    source_pref: str = Field(
        description="Preferred source type (e.g., 'academic', 'industry', 'news', 'mixed')."
    )
    freshness_window: str = Field(
        description="Target recency window (e.g., '≤18 months', '2024-2025', '≤2 years')."
    )
    reasoning: str = Field(
        description="Brief explanation of why this query is important for the research brief."
    )


class ResearchPlan(BaseModel):
    """Output from the query planner agent containing research tasks."""

    tasks: List[ResearchTask] = Field(
        description="List of research tasks to execute.",
        min_length=1,
        max_length=4
    )


class ResearchFinding(BaseModel):
    """An individual finding from SERP collection with metadata."""

    title: str = Field(description="Title of the search result or finding.")
    snippet: str = Field(
        description="Snippet or description text from the source."
    )
    credibility_guess: str = Field(
        description="Initial credibility assessment (high/medium/low) based on domain and context."
    )


class ResearchBatch(BaseModel):
    """Collection of findings from all research tasks."""

    findings: List[ResearchFinding] = Field(
        description="All collected research findings across all tasks."
    )


__all__ = [
    "ResearchTask",
    "ResearchPlan",
    "ResearchFinding",
    "ResearchBatch",
]