import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the environment variables
load_dotenv()

# 2. Get the key
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ ERROR: The API key is empty! .env is not loading correctly.")
else:
    print(f"✅ Key loaded successfully (starts with: {api_key[:10]}...)")
    
    # 3. Try a tiny, cheap request
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    
    try:
        print("⏳ Sending test request to OpenRouter...")
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", # A very standard, reliable model for testing
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=5
        )
        print(f"🎉 SUCCESS! The model replied: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"💥 API CALL FAILED! Here is the exact error:\n{e}")