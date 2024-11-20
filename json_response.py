import requests
import json

# Initialize Ollama endpoint and API token (replace with actual URL/token if required)
OLLAMA_API_URL = "https://api.ollama.com/v1/chat"
API_TOKEN = "YOUR_API_TOKEN"  # Replace with your actual API token if required

def chat_with_qwen(message, history):
    # Format the conversation history and new message
    messages = []
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})
    
    # Prepare headers and payload for API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    payload = {
        "model": "qwen2.5-coder:7b-instruct",
        "messages": messages,
        "stream": False
    }

    # Send POST request to Ollama API
    response = requests.post(OLLAMA_API_URL, headers=headers, json=payload)
    
    # Handle the JSON response
    if response.status_code == 200:
        response_json = response.json()
        return response_json  # Return the entire JSON response if needed
    else:
        return {"error": f"Failed to get response: {response.status_code}", "details": response.text}

# Example usage
if __name__ == "__main__":
    # Example conversation history
    history = [("Write a Python function to sort a list", "Sure, here is a function for that: ...")]
    new_message = "Explain how async/await works in JavaScript"
    
    # Call the function
    json_response = chat_with_qwen(new_message, history)
    
    # Print the JSON response
    print(json.dumps(json_response, indent=2))
