from dotenv import load_dotenv
import os
import time
from openai import OpenAI

# Load OPENROUTER_API_KEY from .env
load_dotenv()
api_key = os.environ["OPENROUTER_API_KEY"]

# Point the OpenAI client at OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

QUESTION = "What is the capital of France?"

MODELS = [
    "openai/gpt-5.5",
    "anthropic/claude-opus-4.8",
    "google/gemini-3.1-pro",
    "qwen/qwen-3.7",
]

# Pricing per 1M tokens (input, output) in USD
PRICING = {
    "openai/gpt-5.5":           (5.00,  30.00),
    "anthropic/claude-opus-4.8": (5.00,  25.00),
    "google/gemini-3.1-pro":    (1.25,   5.00),
    "qwen/qwen-3.7":            (0.40,   0.40),
}


def ask(question, model):
    in_rate, out_rate = PRICING[model]

    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        max_tokens=150,
    )
    latency = time.time() - start

    in_tokens = response.usage.prompt_tokens
    out_tokens = response.usage.completion_tokens
    cost = (in_tokens * in_rate / 1_000_000) + (out_tokens * out_rate / 1_000_000)
    text = response.choices[0].message.content

    return text, latency, in_tokens, out_tokens, cost


for model in MODELS:
    text, latency, in_tok, out_tok, cost = ask(QUESTION, model)
    print(f"Model:    {model}")
    print(f"Answer:   {text}")
    print(f"Latency:  {latency:.2f}s")
    print(f"Tokens:   {in_tok} in / {out_tok} out")
    print(f"Cost:     ${cost:.6f}")
    print()
