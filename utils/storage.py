"""
Generalized storage utilities for saving any agent's output to local storage.

Following Google ADK best practices for artifact persistence.
This module provides a reusable callback function that works with any agent
that uses output_key to save its results.
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


async def save_agent_output_to_file(
    callback_context: CallbackContext,
    output_key: Optional[str] = None,
    output_dir: Optional[Path] = None,
    filename_prefix: Optional[str] = None
) -> Optional["types.Content"]:
    """
    Generalized callback function to save any agent's output to local JSON file.
    
    Using after_agent_callback to persist agent outputs to local storage after execution.
    This function works with any agent that uses output_key to save its results.
    
    Args:
        callback_context: The callback context from ADK
        output_key: The key in state where the output is stored. If None, attempts
                    to auto-detect by looking for the most recent dict/list in state.
        output_dir: Optional directory path. If None, uses default data/collections
        filename_prefix: Optional prefix for the filename. If None, uses output_key
                         or agent_name
         
    Returns:
        None to preserve the agent's original output
    """
    try:
        # Get state
        state = callback_context.state.to_dict()
        agent_name = callback_context.agent_name
        invocation_id = callback_context.invocation_id
        
        # Determine output_key if not provided
        if output_key is None:
            # Try to find the most likely output key
            # Look for keys that contain structured data (dict or list)
            # Exclude internal/metadata keys
            candidate_keys = []
            for key, value in state.items():
                if isinstance(value, (dict, list)) and not key.startswith('_'):
                    # Prefer keys that look like output keys (not metadata)
                    if key not in ['_metadata', '_history', 'temp']:
                        candidate_keys.append((key, value))
            
            if candidate_keys:
                # Use the first candidate (usually the most recent)
                output_key = candidate_keys[0][0]
                print(f"[Storage] Auto-detected output_key: {output_key} for agent {agent_name}")
            else:
                print(f"[Storage] WARNING: Could not auto-detect output_key for agent {agent_name}")
                print(f"[Storage] Available state keys: {list(state.keys())}")
                return None
        
        # Get the output data from state
        output_data_raw = state.get(output_key)
        
        if output_data_raw is None:
            print(f"[Storage] WARNING: Output key '{output_key}' not found in state for agent {agent_name}!")
            print(f"[Storage] Available state keys: {list(state.keys())}")
            return None
        
        # Ensure output directory exists
        if output_dir is None:
            output_dir = ensure_output_directory()
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = filename_prefix or output_key or agent_name
        filename = f"{prefix}_{timestamp}.json"
        filepath = output_dir / filename
        
        # Convert Pydantic model to dict if needed
        if hasattr(output_data_raw, 'model_dump'):
            output_data = output_data_raw.model_dump()
        elif hasattr(output_data_raw, 'dict'):
            output_data = output_data_raw.dict()
        else:
            output_data = output_data_raw
        
        # Create metadata wrapper
        saved_data = {
            "timestamp": timestamp,
            "invocation_id": invocation_id,
            "agent_name": agent_name,
            "output_key": output_key,
            "output": output_data
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(saved_data, f, indent=2, ensure_ascii=False)
        
        print(f"[Storage] Successfully saved {agent_name} output (key: {output_key}) to {filepath}")
        
        return None  # Preserve original agent output
        
    except Exception as e:
        print(f"[Storage] Error saving agent output to file: {e}")
        import traceback
        traceback.print_exc()
        return None  # Don't break the agent execution
