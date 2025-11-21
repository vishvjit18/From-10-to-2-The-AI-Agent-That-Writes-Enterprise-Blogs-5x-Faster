"""
Storage utilities for saving agent outputs to local storage.

Following Google ADK best practices for artifact persistence.
"""

import json
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from google.adk.agents.callback_context import CallbackContext

if TYPE_CHECKING:
    from google.genai import types


def ensure_output_directory() -> Path:
    """Ensure the output directory exists for saving agent outputs."""
    output_dir = Path("data/collections")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


async def save_research_plan_to_file(
    callback_context: CallbackContext,
    output_dir: Optional[Path] = None
) -> Optional[types.Content]:
    """
    Callback function to save research_plan output to local JSON file.
    
    Using after_agent_callback to persist agent outputs to local storage after execution.
    
    Args:
        callback_context: The callback context from ADK
        output_dir: Optional directory path. If None, uses default data/collections
        
    Returns:
        None to preserve the agent's original output
    """
    try:
        # Get state
        state = callback_context.state.to_dict()
        
        # Try to get research_plan from state (saved via output_key)
        research_plan = state.get("research_plan")
        
        if research_plan is None:
            print("[Storage] WARNING: research_plan not found in state!")
            print("[Storage] This might mean:")
            print("  1. The output_key hasn't saved to state yet")
            print("  2. The output is under a different key")
            print("  3. There was an error in agent execution")
            
            # Try to find any JSON-like data in state
            for key, value in state.items():
                if isinstance(value, dict) and 'tasks' in value:
                    print(f"[Storage] Found potential research_plan under key: {key}")
                    research_plan = value
                    break
            
            if research_plan is None:
                return None
        
        # Ensure output directory exists
        if output_dir is None:
            output_dir = ensure_output_directory()
        
        # Generate filename with timestamp and invocation_id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        invocation_id = callback_context.invocation_id
        filename = f"research_plan_{invocation_id}_{timestamp}.json"
        filepath = output_dir / filename
        
        # Convert Pydantic model to dict if needed
        if hasattr(research_plan, 'model_dump'):
            plan_data = research_plan.model_dump()
        elif hasattr(research_plan, 'dict'):
            plan_data = research_plan.dict()
        else:
            plan_data = research_plan
        
        # Add metadata
        output_data = {
            "timestamp": timestamp,
            "invocation_id": invocation_id,
            "agent_name": callback_context.agent_name,
            "research_plan": plan_data
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"[Storage] Successfully saved research_plan to {filepath}")
        
        return None  # Preserve original agent output
        
    except Exception as e:
        print(f"[Storage] Error saving research_plan to file: {e}")
        return None  # Don't break the agent execution
