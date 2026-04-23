import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "your_google_api_key_here":
    print("ERROR: Please set your actual GOOGLE_API_KEY in the .env file!")
    exit()

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
print("Fetching available models from Google AI Studio...")

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        models = data.get('models', [])
except urllib.error.URLError as e:
    print(f"API Error: {e}")
    print("\nThis usually means your API key is invalid or your Google Cloud Project doesn't have the Generative Language API enabled.")
    models = []

if models:
    valid_models = []
    for m in models:
        # We only want models that support text generation (used by LangChain chat models)
        if 'generateContent' in m.get('supportedGenerationMethods', []):
            valid_models.append(m['name'].replace('models/', ''))
            
    if not valid_models:
        print("Your API key is valid, but it has NO ACCESS to any generation models.")
    else:
        print("\nSUCCESS! Your API key has access to the following models:")
        for vm in valid_models:
            print(f" - {vm}")
        print("\nPlease pick one of the models above (like 'gemini-1.5-flash' or 'gemini-2.0-flash') and update src/nodes.py with it.")
