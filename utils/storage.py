"""
Generalized storage utilities for saving any agent's output to local storage.

Following Google ADK best practices for artifact persistence.
This module provides a reusable callback function that works with any agent
that uses output_key to save its results.
"""

import json
from functools import partial
from pathlib import Path
from typing import Optional, TYPE_CHECKING, Callable, Dict, Any, Tuple
from datetime import datetime

from google.adk.agents.callback_context import CallbackContext

if TYPE_CHECKING:
    from google.genai import types


def _ensure_output_dir(output_dir: Optional[Path] = None) -> Path:
    """Ensure the output directory exists for saving agent outputs."""
    if output_dir is None:
        output_dir = Path("data/collections")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _get_context_info(callback_context: CallbackContext) -> Tuple[Dict[str, Any], str, str]:
    """Extract common context information from callback context."""
    state = callback_context.state.to_dict()
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    return state, agent_name, invocation_id


def _detect_output_key(
    state: Dict[str, Any],
    agent_name: str,
    output_type: str = "structured"
) -> Optional[str]:
    """
    Auto-detect output_key from state based on output type.
    
    Args:
        state: The agent state dictionary
        agent_name: Name of the agent (for logging)
        output_type: "structured" (dict/list) or "markdown" (string)
        
    Returns:
        Detected output_key or None if not found
    """
    candidate_keys = []
    excluded_keys = ['_metadata', '_history', 'temp']
    
    for key, value in state.items():
        if key.startswith('_') or key in excluded_keys:
            continue
            
        if output_type == "structured" and isinstance(value, (dict, list)):
            candidate_keys.append((key, value))
        elif output_type == "markdown" and isinstance(value, str):
            candidate_keys.append((key, value))
    
    if candidate_keys:
        output_key = candidate_keys[0][0]
        print(f"[Storage] Auto-detected output_key: {output_key} for agent {agent_name}")
        return output_key
    else:
        print(f"[Storage] WARNING: Could not auto-detect output_key for agent {agent_name}")
        print(f"[Storage] Available state keys: {list(state.keys())}")
        return None


def _build_filepath(
    output_dir: Path,
    filename_prefix: Optional[str],
    output_key: Optional[str],
    agent_name: str,
    extension: str,
    timestamp: str
) -> Path:
    """Build filepath with timestamp and appropriate extension."""
    prefix = filename_prefix or output_key or agent_name
    filename = f"{prefix}.{extension}"
    return output_dir / filename


def _extract_from_pydantic(data: Any) -> Any:
    """
    Extract data from Pydantic models using consistent strategy.
    
    Tries model_dump() first (Pydantic v2), then dict() (Pydantic v1),
    otherwise returns the data as-is.
    
    Args:
        data: Potentially a Pydantic model or any other data
        
    Returns:
        Extracted dict/data from Pydantic model, or original data
    """
    if hasattr(data, 'model_dump'):
        return data.model_dump()
    elif hasattr(data, 'dict'):
        return data.dict()
    else:
        return data


def _extract_text_fields(data: Dict[str, Any]) -> str:
    """
    Extract text content from a dictionary using consistent field priority.
    
    Checks for common text field names in order of preference:
    1. 'content' - most common field name
    2. 'text' - alternative text field
    3. 'markdown' - markdown-specific field
    
    If none found, returns string representation of the entire dict.
    
    Args:
        data: Dictionary to extract text from
        
    Returns:
        Extracted text string, or string representation of data if no text fields found
    """
    if not isinstance(data, dict):
        return str(data)
    
    # Priority order for text fields - can be extended easily
    text_fields = ['content', 'text', 'markdown']
    
    for field in text_fields:
        value = data.get(field)
        if value is not None and isinstance(value, str):
            return value
    
    # Fallback to string representation of entire dict
    return str(data)


def _normalize_structured_output(output_data_raw: Any) -> Any:
    """Convert Pydantic models or other structured data to dict."""
    return _extract_from_pydantic(output_data_raw)


def _normalize_markdown_output(output_data_raw: Any) -> str:
    """Convert various data types to markdown string."""
    # First, try to extract from Pydantic models
    extracted = _extract_from_pydantic(output_data_raw)
    
    # If extracted data is a dict, try to find text fields
    if isinstance(extracted, dict):
        return _extract_text_fields(extracted)
    
    # If it's already a string, return it
    if isinstance(extracted, str):
        return extracted
    
    # Otherwise, convert to string
    return str(extracted)


def _create_json_metadata(
    timestamp: str,
    invocation_id: str,
    agent_name: str,
    output_key: str,
    output_data: Any
) -> Dict[str, Any]:
    """Create metadata wrapper for JSON output."""
    return {
        "timestamp": timestamp,
        "invocation_id": invocation_id,
        "agent_name": agent_name,
        "output_key": output_key,
        "output": output_data
    }


def _create_markdown_frontmatter(
    timestamp: str,
    invocation_id: str,
    agent_name: str,
    output_key: str
) -> str:
    """Create YAML frontmatter for markdown output."""
    return f"""---
timestamp: {timestamp}
invocation_id: {invocation_id}
agent_name: {agent_name}
output_key: {output_key}
---

"""


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
        # Get context information
        state, agent_name, invocation_id = _get_context_info(callback_context)
        
        # Auto-detect output_key if not provided
        if output_key is None:
            output_key = _detect_output_key(state, agent_name, output_type="structured")
            if output_key is None:
                return None
        
        # Get the output data from state
        output_data_raw = state.get(output_key)
        if output_data_raw is None:
            print(f"[Storage] WARNING: Output key '{output_key}' not found in state for agent {agent_name}!")
            print(f"[Storage] Available state keys: {list(state.keys())}")
            return None
        
        # Ensure output directory exists
        output_dir = _ensure_output_dir(output_dir)
        
        # Generate timestamp once for both filepath and metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Build filepath
        filepath = _build_filepath(output_dir, filename_prefix, output_key, agent_name, "json", timestamp)
        
        # Normalize structured output
        output_data = _normalize_structured_output(output_data_raw)
        
        # Create metadata wrapper
        saved_data = _create_json_metadata(timestamp, invocation_id, agent_name, output_key, output_data)
        
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


def create_storage_callback(output_key: str) -> Callable:
    """
    Creates a storage callback function with the output_key pre-bound.
    
    This ensures that each agent's output is saved using its specific output_key,
    preventing auto-detection from picking up keys from previous agents in a sequence.
    
    Args:
        output_key: The output_key that the agent uses to store its results
        
    Returns:
        A callback function that can be used as after_agent_callback
    """
    return partial(save_agent_output_to_file, output_key=output_key)


async def save_agent_output_to_markdown_file(
    callback_context: CallbackContext,
    output_key: Optional[str] = None,
    output_dir: Optional[Path] = None,
    filename_prefix: Optional[str] = None
) -> Optional["types.Content"]:
    """
    Generalized callback function to save any agent's markdown output to local .md file.
    
    Using after_agent_callback to persist agent markdown outputs to local storage after execution.
    This function works with any agent that outputs markdown content (strings).
    
    Args:
        callback_context: The callback context from ADK
        output_key: The key in state where the markdown output is stored. If None, attempts
                    to auto-detect by looking for the most recent string in state.
        output_dir: Optional directory path. If None, uses default data/collections
        filename_prefix: Optional prefix for the filename. If None, uses output_key
                         or agent_name
         
    Returns:
        None to preserve the agent's original output
    """
    try:
        # Get context information
        state, agent_name, invocation_id = _get_context_info(callback_context)
        
        # Auto-detect output_key if not provided
        if output_key is None:
            output_key = _detect_output_key(state, agent_name, output_type="markdown")
            if output_key is None:
                return None
        
        # Get the output data from state
        output_data_raw = state.get(output_key)
        if output_data_raw is None:
            print(f"[Storage] WARNING: Output key '{output_key}' not found in state for agent {agent_name}!")
            print(f"[Storage] Available state keys: {list(state.keys())}")
            return None
        
        # Ensure output directory exists
        output_dir = _ensure_output_dir(output_dir)
        
        # Generate timestamp once for both filepath and metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Build filepath
        filepath = _build_filepath(output_dir, filename_prefix, output_key, agent_name, "md", timestamp)
        
        # Normalize markdown output
        markdown_content = _normalize_markdown_output(output_data_raw)
        
        # Create YAML frontmatter for metadata
        frontmatter = _create_markdown_frontmatter(timestamp, invocation_id, agent_name, output_key)
        
        # Combine frontmatter with markdown content
        full_content = frontmatter + markdown_content
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"[Storage] Successfully saved {agent_name} markdown output (key: {output_key}) to {filepath}")
        
        return None  # Preserve original agent output
        
    except Exception as e:
        print(f"[Storage] Error saving agent markdown output to file: {e}")
        import traceback
        traceback.print_exc()
        return None  # Don't break the agent execution


def create_markdown_storage_callback(output_key: str) -> Callable:
    """
    Creates a markdown storage callback function with the output_key pre-bound.
    
    This ensures that each agent's markdown output is saved using its specific output_key,
    preventing auto-detection from picking up keys from previous agents in a sequence.
    
    Args:
        output_key: The output_key that the agent uses to store its markdown results
        
    Returns:
        A callback function that can be used as after_agent_callback
    """
    return partial(save_agent_output_to_markdown_file, output_key=output_key)