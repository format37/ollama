import requests
import json
import os

# Initialize Ollama endpoint for the LOCAL server
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_API_URL = OLLAMA_BASE_URL + "/api/generate"  # Changed from /api/chat to /api/generate

# Define the Ollama model to use locally
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')

# --- Define the JSON schema (Optional but good for reference) ---
# You might want to add Pydantic models back if you plan to validate the response
# from pydantic import BaseModel, Field
# from typing import List, Optional

# class Experience(BaseModel):
#     company_name: str = Field(description="Name of the company")
#     job_title: str = Field(description="Job title held at the company")
#     years: int = Field(description="Number of years worked at the company")

# class Candidate(BaseModel):
#     name: str = Field(description="Full name of the candidate")
#     email: Optional[str] = Field(description="Email address of the candidate")
#     experience: List[Experience] = Field(description="List of previous work experiences")

# --- Create the prompt for JSON output ---
prompt_for_json = """
Return ONLY a JSON object (without any introductory text or markdown formatting) for a fictional candidate applying for a software engineering role.
The JSON object should include fields like 'name' (string), 'email' (string, optional), and 'experience' (list of objects).
Each experience object should have 'company_name' (string), 'job_title' (string), and 'years' (integer).
Example structure:
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "experience": [
    {"company_name": "Tech Corp", "job_title": "Software Engineer", "years": 3},
    {"company_name": "Innovate LLC", "job_title": "Junior Developer", "years": 2}
  ]
}
"""

# Updated function to use the local endpoint and handle JSON format request
def get_ollama_json_response(prompt: str, model: str = OLLAMA_MODEL):
    # Prepare headers (no Authorization needed for local)
    headers = {
        "Content-Type": "application/json",
    }
    
    # Changed payload structure to match /api/generate endpoint
    payload = {
        "model": model,
        "prompt": prompt,
        "format": "json", # Request JSON format from Ollama
        "stream": False
    }

    print(f"--- Sending request to {OLLAMA_API_URL} with model {model} ---")
    # print(f"Payload: {json.dumps(payload, indent=2)}") # Uncomment for debugging

    try:
        # Send POST request to LOCAL Ollama API
        response = requests.post(OLLAMA_API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        response_json = response.json()
        # Extract the response content
        if 'response' in response_json:
            # Attempt to parse the JSON string
            try:
                json_content = json.loads(response_json['response'])
                return json_content
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON content from Ollama: {e}")
                print(f"Raw content received: {response_json['response']}")
                return {"error": "Failed to decode JSON content from Ollama response", "details": response_json['response']}
        else:
            print("Unexpected response structure:", response_json)
            return {"error": "Unexpected response structure from Ollama", "details": response_json}

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama API at {OLLAMA_API_URL}: {e}")
        return {"error": f"Failed to connect to Ollama: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}


# Example usage for getting JSON candidate data
if __name__ == "__main__":
    print(f"Requesting JSON candidate data using model: {OLLAMA_MODEL}")

    # Call the function with the JSON prompt
    json_response = get_ollama_json_response(prompt_for_json)

    # Print the JSON response
    print("\n--- Received JSON Response ---")
    if "error" in json_response:
        print(f"Error: {json_response['error']}")
        if "details" in json_response:
            print(f"Details: {json_response['details']}")
    else:
        print(json.dumps(json_response, indent=2))

    # Optional: Validate with Pydantic if you uncommented the schema definitions
    # try:
    #     if "error" not in json_response:
    #         candidate = Candidate(**json_response)
    #         print("\n--- Pydantic Validation Successful ---")
    #         print(candidate)
    # except Exception as e:
    #      print(f"\n--- Pydantic Validation Failed ---")
    #      print(e)
