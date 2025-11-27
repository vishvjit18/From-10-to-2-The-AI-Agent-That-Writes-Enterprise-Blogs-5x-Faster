"""
Shared HTTP retry configuration and Gemini model instance.
"""

from google.genai import types
from google.adk.models.google_llm import Gemini


retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,  # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

gemini_model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config,
)

__all__ = ["retry_config", "gemini_model"]


