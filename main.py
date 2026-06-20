from dotenv import load_dotenv
import os
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


def ask(question, model):
    # Send the question to one model and return the text response
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        max_tokens=150,
    )
    return response.choices[0].message.content


for model in MODELS:
    answer = ask(QUESTION, model)
    print(f"{model}: {answer}")
