"""
Blog Writing Pipeline Agent for Blog Writing system.

This agent orchestrates multiple agents sequentially to create a complete blog article:
1. Data Hunter Agent - Plans research and collects data analysis
2. Gap Analyzer Agent - Analyzes SERP and identifies content gaps
3. Article Planner Agent - Creates structured article plan
4. Introduction Writer Agent - Writes introduction section
5. Technical Writer Agent - Writes technical sections
6. Final Formatter Agent - Combines and formats final article
"""

from google.adk.agents import SequentialAgent
from data_hunter_agent.agent import root_agent as data_hunter_agent
from gap_analyzer_agent.agent import root_agent as gap_analyzer_agent
from blog_writing_agent.agent import root_agent as article_planner_agent
from blog_writing_agent.introduction_writer_agent import introduction_writer_agent
from blog_writing_agent.evidence_writer_agent import evidence_writer_agent
from blog_writing_agent.conceptual_writer_agent import conceptual_writer_agent
from blog_writing_agent.conclusion_writer_agent import conclusion_writer_agent
from blog_writing_agent.technical_writer_agent import technical_writer_agent
from blog_writing_agent.final_formatter_agent import final_formatter_agent

# Create SequentialAgent pipeline that runs agents in order
# Each agent's output is stored and can be accessed by subsequent agents via context.state
root_agent = SequentialAgent(
    name="blog_writing_pipeline",
    description=(
        "Orchestrates the complete blog writing workflow: research, gap analysis, planning, "
        "introduction writing, technical writing, and final formatting. Executes agents "
        "sequentially to produce a publication-ready blog article."
    ),
    sub_agents=[
        data_hunter_agent,          # Step 1: Research planning and data collection
        gap_analyzer_agent,         # Step 2: SERP analysis and gap identification
        article_planner_agent,      # Step 3: Create article plan from analysis files
        introduction_writer_agent,  # Step 4: Write introduction section
        evidence_writer_agent,      # Step 5: Write evidence sections
        conceptual_writer_agent,    # Step 6: Write conceptual sections
        conclusion_writer_agent,    # Step 7: Write conclusion section
        technical_writer_agent,     # Step 5: Write technical sections
        final_formatter_agent,      # Step 6: Format final article
    ],
)

