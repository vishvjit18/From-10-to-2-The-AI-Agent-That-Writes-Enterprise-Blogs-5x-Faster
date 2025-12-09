"""
OpenRouter model configuration using LiteLLM for Google ADK integration.

This module provides OpenRouter model instances that can be used with Google ADK agents,
following the same pattern as the Gemini model configuration in retry.py.

Uses LiteLLM wrapper from Google ADK to access OpenRouter models.
Requires OPENROUTER_API_KEY environment variable to be set.
"""

import os
from google.adk.models.lite_llm import LiteLlm

# Default OpenRouter model (free tier)
# Using meta-llama/llama-3.3-70b-instruct:free as default (more reliable)
DEFAULT_OPENROUTER_MODEL = "openrouter/meta-llama/llama-3.3-70b-instruct:free"

# Fallback models (free tier) to try if default model is rate-limited
# Note: Free-tier models may experience rate limits. If you encounter RateLimitError:
# 1. Wait a few minutes and retry
# 2. Use a different model from this list
# 3. Add your own API key at https://openrouter.ai/settings/integrations for higher rate limits
FALLBACK_MODELS = [
    "openrouter/meta-llama/llama-3.1-8b-instruct:free",
    "openrouter/mistralai/mistral-7b-instruct:free",
    "openrouter/google/gemma-2-9b-it:free",
    "openrouter/meta-llama/llama-3.2-3b-instruct:free",
]


def create_openrouter_model(model_name: str = None) -> LiteLlm:
    """
    Create a LiteLLM model instance configured for OpenRouter.
    
    Args:
        model_name: OpenRouter model identifier. If None, uses the default free-tier model.
                   Format: "openrouter/provider/model-name" or "openrouter/provider/model-name:free"
    
    Returns:
        LiteLlm instance configured for OpenRouter that can be used with ADK agents.
    
    Example:
        >>> from utils.openrouter_model import create_openrouter_model
        >>> model = create_openrouter_model()
        >>> agent = LlmAgent(model=model, name="my_agent", instruction="...")
    """
    if model_name is None:
        model_name = DEFAULT_OPENROUTER_MODEL
    
    # Ensure model name starts with "openrouter/" prefix for LiteLLM
    if not model_name.startswith("openrouter/"):
        model_name = f"openrouter/{model_name}"
    
    # Check for API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable is required. "
            "Get your API key from https://openrouter.ai/"
        )
    
    return LiteLlm(model=model_name)


# Pre-configured model instance for convenience (matches pattern from retry.py)
# Note: This will raise ValueError if OPENROUTER_API_KEY is not set at import time
try:
    openrouter_model = create_openrouter_model()
except ValueError:
    # Allow import even if API key is not set (will fail when actually used)
    openrouter_model = None

__all__ = [
    "create_openrouter_model", 
    "openrouter_model", 
    "DEFAULT_OPENROUTER_MODEL",
    "FALLBACK_MODELS"
]




