"""Blog Writing Agent package for producing high-quality blog articles."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class SectionPlan(BaseModel):
    """Plan for a single article section."""
    
    title: str = Field(description="Section title")
    description: str = Field(description="Brief description of what this section covers")
    estimated_word_count: int = Field(description="Estimated word count for this section")
    key_points: List[str] = Field(description="Key points to cover in this section")
    evidence_needs: List[str] = Field(description="Required evidence, statistics, or data for this section")
    technical_depth: str = Field(description="Required technical depth level (e.g., 'high', 'medium', 'low', 'none')")
    practical_examples: List[str] = Field(description="Types of practical examples needed")
    conceptual_distinctions: List[str] = Field(description="Conceptual distinctions to make in this section")
    focus_areas: List[str] = Field(description="Which focus areas this section addresses")


class VisualOpportunity(BaseModel):
    """A visual element opportunity in the article."""
    
    type: str = Field(description="Type of visual (e.g., 'infographic', 'diagram', 'process_flow', 'data_visualization')")
    description: str = Field(description="Description of the visual element")
    suggested_location: str = Field(description="Where in the article this visual should appear")
    purpose: str = Field(description="Purpose of this visual element")


class ArticleOverview(BaseModel):
    """Article overview including target audience, purpose, key message, and differentiation strategy."""
    
    target_audience: str = Field(description="Description of the target audience")
    purpose: str = Field(description="Main purpose of the article")
    key_message: str = Field(description="Core message to convey")
    value_proposition: str = Field(description="Value proposition for readers")
    differentiation_strategy: str = Field(description="Strategy based on identified gaps")


class FocusAreasMapping(BaseModel):
    """Mapping of focus area types to section titles."""
    
    technical_implementation: List[str] = Field(default_factory=list, description="Section titles that address technical implementation")
    evidence_and_metrics: List[str] = Field(default_factory=list, description="Section titles that cover evidence and metrics")
    conceptual_distinctions: List[str] = Field(default_factory=list, description="Section titles that explore conceptual distinctions")
    ethical_considerations: List[str] = Field(default_factory=list, description="Section titles that address ethical considerations")


class ToneAndStyle(BaseModel):
    """Tone and style guidelines for the article."""
    
    professional_tone: str = Field(description="Professional tone requirements")
    technical_accessibility_balance: str = Field(description="Balance between technical depth and accessibility")
    critical_thinking: str = Field(description="Critical thinking and balanced perspective needs")
    evidence_based_approach: str = Field(description="Evidence-based approach requirements")


class ArticlePlan(BaseModel):
    """Structured article plan output from the Article Planner Agent."""
    
    overview: ArticleOverview = Field(description="Article overview including target audience, purpose, key message, and differentiation strategy")
    structure: List[SectionPlan] = Field(description="Detailed article structure with sections and subsections")
    focus_areas_mapping: FocusAreasMapping = Field(description="Mapping of focus areas to section titles")
    visual_opportunities: List[VisualOpportunity] = Field(description="Identified visual opportunities throughout the article")
    tone_and_style: ToneAndStyle = Field(description="Tone and style guidelines for the article")


from .agent import root_agent

__all__ = [
    "root_agent",
    "ArticlePlan",
    "ArticleOverview",
    "FocusAreasMapping",
    "ToneAndStyle"
]

