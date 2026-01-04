import os
import json
import urllib.request
import urllib.error
import ssl

# Workaround for SSL: CERTIFICATE_VERIFY_FAILED
ssl._create_default_https_context = ssl._create_unverified_context

def load_env():
    """Simple parser for .env file to avoid external dependencies."""
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

def call_gemini(prompt_text):
    """
    Sends a synchronous request to the Gemini 1.5 Flash API.
    Returns the text content of the response.
    """
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment or .env file.")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    parsed_data = json.dumps(data).encode("utf-8")
    
    req = urllib.request.Request(url, data=parsed_data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            # improved error handling for empty responses
            try:
                text = result['candidates'][0]['content']['parts'][0]['text']
                return text
            except (KeyError, IndexError):
                return f"Error parsing response: {result}"
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return f"HTTP Error {e.code}: {e.reason}\nDetails: {error_body}"
    except Exception as e:
        return f"Unexpected Error: {e}"

if __name__ == "__main__":
    # Simple test
    print(call_gemini("Hello, are you online?"))
