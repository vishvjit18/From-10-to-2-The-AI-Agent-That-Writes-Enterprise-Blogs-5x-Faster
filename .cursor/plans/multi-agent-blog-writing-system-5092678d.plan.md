<!-- 5092678d-381c-47e6-b3f4-eac8f1a4db12 7254aeb8-46c3-45ab-b15f-aed74abadb4f -->
# Multi-Agent Blog Writing System Implementation

## Overview

Transform the single `blog_writing_agent` into a specialized multi-agent system using Approach 4: Hybrid with Option D content writers. All agents will be generalized (not topic-specific) and follow existing codebase patterns.

## Architecture

The system will use a `SequentialAgent` to orchestrate:

1. **Article Planner Agent** - Creates detailed outline from analysis files
2. **Introduction Writer Agent** - Writes introduction and framework
3. **Technical Writer Agent** - Technical deep-dive sections
4. **Evidence Writer Agent** - Data, metrics, case studies
5. **Conceptual Writer Agent** - Conceptual distinctions and ethical considerations
6. **Conclusion Writer Agent** - Conclusion and synthesis
7. **Visual Strategist Agent** - Adds visual annotations
8. **Quality Assurance Agent** - Quality checks
9. **Final Formatter Agent** - Final formatting

## File Structure

```
blog_writing_agent/
├── __init__.py (updated to export root_agent)
├── agent.py (orchestrator using SequentialAgent)
├── article_planner_agent.py
├── introduction_writer_agent.py
├── technical_writer_agent.py
├── evidence_writer_agent.py
├── conceptual_writer_agent.py
├── conclusion_writer_agent.py
├── visual_strategist_agent.py
├── quality_assurance_agent.py
└── final_formatter_agent.py
```

## Implementation Details

### 1. Article Planner Agent (`article_planner_agent.py`)

- **Input**: Analysis files (data_analysis, gap_analysis)
- **Output**: `article_plan` (structured JSON outline with sections, key points, evidence needs)
- **Storage**: Save to `data/collections/article_plan.json`
- **Schema**: Uses `ArticlePlan` Pydantic model for structured JSON output
- **Generalized instructions**: Analyzes provided analysis files, creates structured JSON plan, identifies content requirements

### 2. Introduction Writer Agent (`introduction_writer_agent.py`)

- **Input**: `{article_plan}`
- **Output**: `introduction_section` (introduction + framework)
- **Storage**: Save to `data/collections/introduction_section.md`
- **Generalized instructions**: Creates compelling introduction, establishes context, sets up article framework

### 3. Technical Writer Agent (`technical_writer_agent.py`)

- **Input**: `{article_plan}`
- **Output**: `technical_sections` (technical deep-dive content)
- **Storage**: Save to `data/collections/technical_sections.md`
- **Generalized instructions**: Writes technical sections with architecture details, implementation specifics, system design

### 4. Evidence Writer Agent (`evidence_writer_agent.py`)

- **Input**: `{article_plan}`
- **Output**: `evidence_sections` (data-driven content)
- **Storage**: Save to `data/collections/evidence_sections.md`
- **Generalized instructions**: Writes evidence-based sections with metrics, statistics, case studies, quantitative data

### 5. Conceptual Writer Agent (`conceptual_writer_agent.py`)

- **Input**: `{article_plan}`
- **Output**: `conceptual_sections` (conceptual distinctions and analysis)
- **Storage**: Save to `data/collections/conceptual_sections.md`
- **Generalized instructions**: Writes conceptual sections with distinctions, comparisons, ethical considerations, balanced analysis

### 6. Conclusion Writer Agent (`conclusion_writer_agent.py`)

- **Input**: `{article_plan}`
- **Output**: `conclusion_section` (conclusion and synthesis)
- **Storage**: Save to `data/collections/conclusion_section.md`
- **Generalized instructions**: Creates conclusion that synthesizes key points, forward-looking perspective

### 7. Visual Strategist Agent (`visual_strategist_agent.py`)

- **Input**: All previous sections (`{introduction_section}`, `{technical_sections}`, etc.)
- **Output**: `content_with_visuals` (content with visual annotations)
- **Storage**: Save to `data/collections/content_with_visuals.md`
- **Generalized instructions**: Reviews content, identifies visual opportunities, adds markdown comments for infographics/diagrams

### 8. Quality Assurance Agent (`quality_assurance_agent.py`)

- **Input**: `{content_with_visuals}`, `{article_plan}`
- **Output**: `quality_checked_article` (verified content)
- **Storage**: Save to `data/collections/quality_checked_article.md`
- **Generalized instructions**: Verifies all requirements met, checks tone consistency, ensures differentiation strategy, validates focus areas coverage

### 9. Final Formatter Agent (`final_formatter_agent.py`)

- **Input**: `{quality_checked_article}`
- **Output**: `blog_article` (publication-ready article)
- **Storage**: Save to `data/collections/blog_article.md` (existing callback)
- **Generalized instructions**: Final markdown formatting, structure optimization, professional formatting

### 10. Root Orchestrator (`agent.py`)

- **Type**: `SequentialAgent`
- **Sub-agents**: All 10 agents in sequence
- **Pattern**: Follows `data_hunter_agent` and `gap_analyzer_agent` patterns
- **Loads analysis files**: Keep existing `_load_analysis_files()` function
- **Passes analysis files**: Via instruction placeholders `{data_analysis_placeholder}` and `{gap_analysis_placeholder}` to planner only

## Key Design Decisions

1. **Generalization**: All instructions remove topic-specific references (AI agents, creative writing, etc.) and use generic placeholders
2. **Storage**: All intermediate outputs saved to `data/collections/` with descriptive filenames
3. **State Management**: Each agent uses unique `output_key` to avoid conflicts
4. **Instruction Placeholders**: Agents reference previous outputs using `{output_key}` syntax
5. **Model Selection**: Use gemini-2.5-flash-lite for all agents (or can vary by agent type)
6. **Analysis Files**: Only Article Planner receives analysis files; other agents work from the plan

## Migration Strategy

1. Create new agent files following existing patterns
2. Extract and generalize instructions from current monolithic agent
3. Update `agent.py` to use `SequentialAgent` orchestration
4. Test that final output matches expected format
5. Keep backward compatibility in `__init__.py` (still exports `root_agent`)

## Testing Considerations

- Verify all intermediate files are saved correctly
- Ensure final `blog_article` output maintains quality
- Check that all agents receive correct inputs from previous agents
- Validate markdown formatting throughout pipeline

### To-dos

- [x] Create article_planner_agent.py with generalized instructions that analyze analysis files and create structured outline