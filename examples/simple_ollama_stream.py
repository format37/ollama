import requests
import json

def stream_ollama(prompt, model="llama3"):
    """
    Send a prompt to a local Ollama server and stream the response.
    
    Args:
        prompt: The text prompt to send
        model: The model to use (default is "llama3")
    """
    
    # Ollama API endpoint for generation
    url = "http://localhost:11434/api/generate"
    
    # Prepare the request payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }
    
    # Send the request to Ollama and stream the response
    with requests.post(url, json=payload, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    
                    # Print the chunk of text without a newline
                    print(chunk["response"], end="", flush=True)
                    
                    # Check if it's the last chunk
                    if chunk.get("done", False):
                        print("\n")  # Add a newline at the end
                        break
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Example prompt
    prompt = "Explain quantum computing in simple terms."
    
    print(f"Sending prompt to Ollama: \"{prompt}\"\n")
    print("Response from Ollama:")
    
    # Stream response from Ollama
    stream_ollama(prompt) 