"""
Experimental Gemini model wrapper for key-rotation experiments.

Right now this simply re-uses the shared `gemini_model` from `utils.retry`,
so behaviour is identical. You can later replace `rotating_gemini_model`
with a custom implementation that swaps API keys between attempts.
"""

from .retry import gemini_model


rotating_gemini_model = gemini_model

__all__ = ["rotating_gemini_model"]



