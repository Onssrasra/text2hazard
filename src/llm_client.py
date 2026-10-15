"""Small NVIDIA API helper based on the course notebook."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA


DEFAULT_MODEL = "openai/gpt-oss-20b"
MAX_OUTPUT_TOKENS = 4096
REQUEST_TIMEOUT_SECONDS = 180
REASONING_EFFORT = "low"


def create_llm(model: str = DEFAULT_MODEL) -> ChatNVIDIA:
    """Create the model used by both workflows."""

    load_dotenv()
    api_key = os.getenv("NVIDIA_TOKEN")
    if not api_key:
        raise RuntimeError(
            "NVIDIA_TOKEN is missing. Copy .env.example to .env and add your key."
        )

    return ChatNVIDIA(
        model=model,
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
        temperature=0.01,
        seed=42,
        max_tokens=MAX_OUTPUT_TOKENS,
        timeout=REQUEST_TIMEOUT_SECONDS,
        model_kwargs={"reasoning_effort": REASONING_EFFORT},
    )

