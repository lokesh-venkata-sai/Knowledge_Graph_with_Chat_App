import os
import json
import requests

BASE_URL = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')

# Generate a response for a given prompt with a provided model.
def generate(model_name, prompt, system=None, template=None, context=None, options=None, callback=None):
    try:
        url = f"{BASE_URL}/api/generate"
        payload = {
            "model": model_name, 
            "prompt": prompt, 
            "system": system, 
            "template": template, 
            "context": context, 
            "options": options
        }
        
        # Remove keys with None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            
            # Creating a variable to hold the context history of the final chunk
            final_context = None
            
            # Variable to hold concatenated response strings if no callback is provided
            full_response = ""

            # Iterating over the response line by line and displaying the details
            for line in response.iter_lines():
                if line:
                    # Parsing each line (JSON chunk) and extracting the details
                    chunk = json.loads(line)
                    
                    # If a callback function is provided, call it with the chunk
                    if callback:
                        callback(chunk)
                    else:
                        # If this is not the last chunk, add the "response" field value to full_response and print it
                        if not chunk.get("done"):
                            response_piece = chunk.get("response", "")
                            full_response += response_piece
                            print(response_piece, end="", flush=True)
                    
                    # Check if it's the last chunk (done is true)
                    if chunk.get("done"):
                        final_context = chunk.get("context")
            
            # Return the full response and the final context
            return full_response, final_context
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

# List models that are available locally.
def list():
    try:
        response = requests.get(f"{BASE_URL}/api/tags")
        response.raise_for_status()
        data = response.json()
        models = data.get('models', [])
        return models

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def test():
    try:
        url = f"{BASE_URL}/"
        response = requests.head(url)
        response.raise_for_status()
        return "Ollama is running"
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "Ollama is not running"