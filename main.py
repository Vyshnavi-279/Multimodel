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

# Send the question to one model and print the answer
response = client.chat.completions.create(
    model="anthropic/claude-opus-4.8",
    messages=[{"role": "user", "content": QUESTION}],
    max_tokens=150,  # 👈 Add this line to limit the token request
)

print(response.choices[0].message.content)
