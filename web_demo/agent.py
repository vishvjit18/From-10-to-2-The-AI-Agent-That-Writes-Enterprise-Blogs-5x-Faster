"""
Blog Writing Pipeline Agent for Blog Writing system.

This agent orchestrates multiple agents to create a complete blog article:
1. Data Hunter Agent - Plans research and collects data analysis
2. Gap Analyzer Agent - Analyzes SERP and identifies content gaps
3. Article Planner Agent - Creates structured article plan
4. Parallel Writer Agents (runs concurrently):
   - Introduction Writer Agent - Writes introduction section
   - Evidence Writer Agent - Writes evidence sections
   - Conceptual Writer Agent - Writes conceptual sections
   - Conclusion Writer Agent - Writes conclusion section
   - Technical Writer Agent - Writes technical sections
5. Final Formatter Agent - Combines and formats final article
"""

from google.adk.agents import SequentialAgent, ParallelAgent
from data_hunter_agent.agent import root_agent as data_hunter_agent
from gap_analyzer_agent.agent import root_agent as gap_analyzer_agent
from blog_writing_agent.agent import root_agent as article_planner_agent
from blog_writing_agent.introduction_writer_agent import introduction_writer_agent
from blog_writing_agent.evidence_writer_agent import evidence_writer_agent
from blog_writing_agent.conceptual_writer_agent import conceptual_writer_agent
from blog_writing_agent.conclusion_writer_agent import conclusion_writer_agent
from blog_writing_agent.technical_writer_agent import technical_writer_agent
from blog_writing_agent.final_formatter_agent import final_formatter_agent

# Create ParallelAgent for concurrent execution of writer agents
# All writer agents run simultaneously after article planning is complete
# Each agent stores its output in distinct keys in session.state
parallel_writer_agents = ParallelAgent(
    name="parallel_content_writers",
    description=(
        "Executes five specialized writer agents concurrently to create different sections "
        "of the blog article. Each agent works independently on its assigned section type, "
        "significantly reducing total execution time while maintaining content quality."
    ),
    sub_agents=[
        introduction_writer_agent,  # Writes introduction section
        evidence_writer_agent,      # Writes evidence-based sections
        conceptual_writer_agent,    # Writes conceptual sections
        conclusion_writer_agent,    # Writes conclusion section
        technical_writer_agent,     # Writes technical sections
    ],
)

# Create SequentialAgent pipeline that orchestrates the complete workflow
# Sequential stages: research -> analysis -> planning -> parallel writing -> formatting
# Each agent's output is stored and can be accessed by subsequent agents via context.state
root_agent = SequentialAgent(
    name="blog_writing_pipeline",
    description=(
        "Orchestrates the complete blog writing workflow: research, gap analysis, planning, "
        "parallel content writing, and final formatting. Executes research and planning agents "
        "sequentially, then runs all writer agents concurrently for efficiency, and finally "
        "synthesizes everything into a publication-ready blog article."
    ),
    sub_agents=[
        data_hunter_agent,          # Step 1: Research planning and data collection
        gap_analyzer_agent,         # Step 2: SERP analysis and gap identification
        article_planner_agent,      # Step 3: Create article plan from analysis files
        parallel_writer_agents,     # Step 4: Execute all writer agents in parallel
        final_formatter_agent,      # Step 5: Format final article from all sections
    ],
)