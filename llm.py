import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# MODELS and PRICES remain the same...
MODELS = ["openai/gpt-5.5", "anthropic/claude-opus-4.8", "google/gemini-3.1-pro", "qwen/qwen-3.7"]
PRICES = { ... } 

# --- NEW: Load multiple keys ---
keys_string = os.getenv("OPENROUTER_API_KEYS", "")
# Fallback to single key if the plural variable isn't found
if not keys_string:
    keys_string = os.getenv("OPENROUTER_API_KEY", "")

API_KEYS = [k.strip() for k in keys_string.split(",") if k.strip()]

if not API_KEYS:
    raise ValueError("No API keys found in .env file!")

def ask(question, model, api_key_override=None):
    """
    Sends a question to a model. 
    Uses an override key if provided, otherwise picks a random key from the pool.
    """
    # Pick the key to use for this specific call
    key_to_use = api_key_override or random.choice(API_KEYS)
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key_to_use,
    )
    
    start_time = time.time()
    try:
        # ... rest of your existing OpenAI client call logic ...
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            timeout=30.0
        )
        # ... calculate latency, cost, etc ...
        
    except Exception as e:
        # If a specific key fails (e.g., 401 Unauthorized), you could even 
        # add logic here to catch it and retry with a different key!
        raise e