import requests
import json
import time

def call_ollama(prompt, model="llama3.2:3b", stream=False):
    """
    Send a prompt to a local Ollama server and return the response.
    
    Args:
        prompt: The text prompt to send
        model: The model to use (default is "llama3")
        stream: Whether to stream the response (default is False)
        
    Returns:
        The model's response text
    """
    
    # Ollama API endpoint for generation
    url = "http://localhost:11434/api/generate"
    
    # Prepare the request payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    # Send the request to Ollama
    response = requests.post(url, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    # Example prompt
    # prompt = "Explain quantum computing in simple terms."
    prompt = "Пожалуйста, объясните, как работает квантовый компьютер простыми словами."
    print(f"Sending prompt to Ollama: \"{prompt}\"\n")
    
    counter = 0
    start_time = time.time()
    while True:
        iter_start = time.time()
        # Call Ollama and get the response
        response_text = call_ollama(prompt, model="qwen2.5:7b", stream=False)
        iter_end = time.time()
        print(response_text)
        print(f"### Inference counter: {counter}")
        elapsed = iter_end - start_time
        rps = (counter + 1) / elapsed if elapsed > 0 else float('inf')
        print(f"Total elapsed time: {elapsed:.2f} seconds")
        print(f"Average requests per second: {rps:.2f}")
        print(f"Last request time: {iter_end - iter_start:.2f} seconds\n")
        counter += 1
        
    print("Response from Ollama:")
    print(response_text) 