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

from .query_interpreter_agent import query_interpreter_agent
from .serp_collector_agent import serp_collector_agent


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
        "- Query interpretation results: {query_interpretation}\n"
        "- SERP collection results: {serp_results}\n\n"
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
)


# Root agent orchestrates the workflow using SequentialAgent pattern
root_agent = SequentialAgent(
    name="gap_analyzer_agent",
    description=(
        "Analyzes top SERP results for a keyword to summarize themes, "
        "formats, and opportunities for differentiation. Uses specialized "
        "sub-agents for query interpretation and SERP collection."
    ),
    sub_agents=[
        query_interpreter_agent,  # Step 1: Interpret query, expand to search strings
        serp_collector_agent,     # Step 2: Execute searches, collect SERP data
        synthesis_agent,          # Steps 3-4: Synthesize findings and identify gaps
    ],
)

