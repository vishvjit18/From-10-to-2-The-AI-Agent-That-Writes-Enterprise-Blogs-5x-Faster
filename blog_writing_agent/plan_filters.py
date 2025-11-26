"""
Utility functions to filter article plan for specific agent needs.

This module provides filter functions that extract only the relevant parts
of the article plan for each specialized writing agent, reducing token usage
and improving focus.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


def _load_article_plan() -> Dict[str, Any]:
    """
    Load the article plan from JSON file.
    
    Returns:
        Dictionary containing the article plan data, or empty dict if not found.
    """
    data_dir = Path("data/collections")
    article_plan_path = data_dir / "article_plan.json"
    
    if not article_plan_path.exists():
        return {}
    
    try:
        with open(article_plan_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Extract the actual plan from the output field
            return data.get("output", data)
    except Exception as e:
        # Return empty dict on error - agents should handle this gracefully
        return {}


def filter_for_introduction(article_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract only what Introduction Writer needs.
    
    Returns:
        Dictionary containing:
        - overview: Article overview (target_audience, purpose, key_message, etc.)
        - introduction_section: The introduction section plan
        - tone_and_style: Tone and style guidelines
    """
    structure = article_plan.get("structure", [])
    
    # Find introduction section (first section or one with "introduction" in title)
    intro_section = next(
        (s for s in structure if "introduction" in s.get("title", "").lower()),
        structure[0] if structure else {}
    )
    
    return {
        "overview": article_plan.get("overview", {}),
        "introduction_section": intro_section,
        "tone_and_style": article_plan.get("tone_and_style", {})
    }


def filter_for_technical_writer(article_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract sections relevant to Technical Writer.
    
    Returns:
        Dictionary containing:
        - sections: List of sections with technical depth or technical_implementation focus
        - tone_and_style: Tone and style guidelines
        - overview: Minimal overview for context (target_audience, key_message)
    """
    structure = article_plan.get("structure", [])
    
    # Filter sections with technical depth or technical_implementation focus
    technical_sections = [
        s for s in structure 
        if s.get("technical_depth") in ["medium", "high"]
        or "technical_implementation" in s.get("focus_areas", [])
    ]
    
    overview = article_plan.get("overview", {})
    
    return {
        "sections": technical_sections,
        "tone_and_style": article_plan.get("tone_and_style", {}),
        "overview": {  # Minimal overview for context
            "target_audience": overview.get("target_audience", ""),
            "key_message": overview.get("key_message", "")
        }
    }


def filter_for_evidence_writer(article_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract sections that need evidence/data.
    
    Returns:
        Dictionary containing:
        - sections: List of sections with evidence_needs or evidence_and_metrics focus
        - tone_and_style: Tone and style guidelines
        - overview: Minimal overview for context (target_audience, value_proposition)
    """
    structure = article_plan.get("structure", [])
    
    # Filter sections that have evidence needs or evidence_and_metrics focus
    evidence_sections = [
        s for s in structure 
        if s.get("evidence_needs")  # Has evidence needs (non-empty list)
        or "evidence_and_metrics" in s.get("focus_areas", [])
    ]
    
    overview = article_plan.get("overview", {})
    
    return {
        "sections": evidence_sections,
        "tone_and_style": article_plan.get("tone_and_style", {}),
        "overview": {
            "target_audience": overview.get("target_audience", ""),
            "value_proposition": overview.get("value_proposition", "")
        }
    }


def filter_for_conceptual_writer(article_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract sections with conceptual distinctions or ethical considerations.
    
    Returns:
        Dictionary containing:
        - sections: List of sections with conceptual_distinctions or ethical focus
        - tone_and_style: Tone and style guidelines
        - overview: Minimal overview for context (key_message, differentiation_strategy)
    """
    structure = article_plan.get("structure", [])
    
    # Filter sections with conceptual distinctions or ethical considerations
    conceptual_sections = [
        s for s in structure 
        if s.get("conceptual_distinctions")  # Has conceptual distinctions (non-empty list)
        or any(focus in s.get("focus_areas", []) 
               for focus in ["conceptual_distinctions", "ethical_considerations"])
    ]
    
    overview = article_plan.get("overview", {})
    
    return {
        "sections": conceptual_sections,
        "tone_and_style": article_plan.get("tone_and_style", {}),
        "overview": {
            "key_message": overview.get("key_message", ""),
            "differentiation_strategy": overview.get("differentiation_strategy", "")
        }
    }


def filter_for_conclusion_writer(article_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract what Conclusion Writer needs.
    
    Returns:
        Dictionary containing:
        - overview: Minimal overview (key_message, value_proposition)
        - conclusion_section: The conclusion section plan (typically last section)
        - tone_and_style: Tone and style guidelines
    """
    structure = article_plan.get("structure", [])
    
    # Last section is typically conclusion, or find one with "conclusion" in title
    conclusion_section = next(
        (s for s in reversed(structure) if "conclusion" in s.get("title", "").lower()),
        structure[-1] if structure else {}
    )
    
    overview = article_plan.get("overview", {})
    
    return {
        "overview": {
            "key_message": overview.get("key_message", ""),
            "value_proposition": overview.get("value_proposition", "")
        },
        "conclusion_section": conclusion_section,
        "tone_and_style": article_plan.get("tone_and_style", {})
    }


def filter_for_visual_strategist(article_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract visual opportunities and all sections for context.
    
    Returns:
        Dictionary containing:
        - visual_opportunities: List of all visual opportunities
        - structure: All sections (for understanding context where visuals should appear)
        - overview: Article overview (for understanding article purpose)
    """
    return {
        "visual_opportunities": article_plan.get("visual_opportunities", []),
        "structure": article_plan.get("structure", []),  # All sections for context
        "overview": article_plan.get("overview", {})  # For understanding article purpose
    }


def filter_for_quality_assurance(article_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract full article plan for Quality Assurance Agent.
    
    Quality Assurance needs the complete plan to verify all requirements are met.
    
    Returns:
        Complete article plan dictionary (no filtering).
    """
    return article_plan













