"""Environment guard for Evolution Studio."""

import os
from dotenv import load_dotenv

# Load variables from the local env link (if present)
load_dotenv(".env.local")


def require_env(name: str) -> str:
    """Return env var value or fail fast if it is missing."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing env var: {name}")
    return value


GROQ_API_KEY = require_env("GROQ_API_KEY")
OPENAI_API_KEY = require_env("OPENAI_API_KEY")
