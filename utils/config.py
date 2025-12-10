import os
import yaml
from typing import Any, Dict

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file and override with environment variables.
    Environment variables take precedence over YAML values.
    """
    # Go up one level from utils to find config.yaml if strictly relative to this file?
    # Or assume CWD is project root. Usually CWD is project root when running the app.
    # We will try to find config.yaml in CWD first.
    
    config = {}
    
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            try:
                config = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                print(f"Warning: Error parsing {config_path}: {e}")
    
    # Known keys that we expect
    known_keys = ["OPENROUTER_API_KEY", "GOOGLE_API_KEY"]
    
    # Override with environment variables
    for key in known_keys:
        env_val = os.getenv(key)
        if env_val:
            config[key] = env_val
            
    # Also ensure any other keys in the loaded config get overridden if env var exists
    for key in list(config.keys()):
        env_val = os.getenv(key)
        if env_val:
            config[key] = env_val
            
    return config

# Load config instance
config = load_config()
