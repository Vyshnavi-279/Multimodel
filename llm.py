import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODELS = [
    "openai/gpt-5.5",
    "anthropic/claude-opus-4.8",
    "google/gemini-2.5-pro",
    "qwen/qwen-3.7",
]

PRICES = {
    "openai/gpt-5.5":            {"input": 5.00,  "output": 30.00},
    "anthropic/claude-opus-4.8": {"input": 5.00,  "output": 25.00},
    "google/gemini-2.5-pro":     {"input": 1.25,  "output": 10.00},
    "qwen/qwen-3.7":             {"input": 0.40,  "output":  0.40},
}

# Support a comma-separated OPENROUTER_API_KEYS pool, or fall back to the single key
keys_string = os.getenv("OPENROUTER_API_KEYS", "") or os.getenv("OPENROUTER_API_KEY", "")
API_KEYS = [k.strip() for k in keys_string.split(",") if k.strip()]

if not API_KEYS:
    raise ValueError("No API keys found in .env file!")


def ask(question, model, api_key_override=None):
    key_to_use = api_key_override or random.choice(API_KEYS)
    rates = PRICES[model]

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key_to_use,
    )

    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        max_tokens=150,  # keeps requests within free-tier credit budget
        timeout=30.0,
    )
    latency = time.time() - start_time

    in_tokens = response.usage.prompt_tokens
    out_tokens = response.usage.completion_tokens
    cost = (in_tokens * rates["input"] / 1_000_000) + (out_tokens * rates["output"] / 1_000_000)

    return {
        "answer":     response.choices[0].message.content,
        "latency":    latency,
        "in_tokens":  in_tokens,
        "out_tokens": out_tokens,
        "cost":       cost,
    }
