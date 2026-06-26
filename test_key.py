import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ ERROR: The API key is empty! .env is not loading correctly.")
else:
    print(f"✅ Key loaded successfully (starts with: {api_key[:10]}...)")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
    try:
        print("⏳ Sending test request to OpenRouter...")
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", 
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=5
        )
        print(f"🎉 SUCCESS! The model replied: {response.choices[0].message.content}")
    except Exception as e:
        print(f"💥 API CALL FAILED! Here is the exact error:\n{e}")
