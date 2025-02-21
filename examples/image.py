import base64
import requests
import json
from datetime import datetime as dt

def encode_image_to_base64(image_path):
    """Encodes an image file to a base64 string."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

def main():
    # Replace with the path to your image file
    image_path = "./image.jpg"
    # Replace with your text prompt
    prompt = "What's in this image?"

    _prompt = """You are robot. You can see, speak and move.
The available movements are:
- Left track: speed 0-100, direction (0=forward, 1=backward)
- Right track: speed 0-100, direction (0=forward, 1=backward)
- Head position: angle 0-180 degrees (0=full left, 90=center, 180=full right)

Answer in JSON format:
{
    "thoughts": "<describe your thinking process>",
    "speech": "<what you want to say>",
    "movement": {
        "left_track": {
            "speed": <0-100>,
            "direction": <0 or 1>
        },
        "right_track": {
            "speed": <0-100>,
            "direction": <0 or 1>
        },
        "head": {
            "angle": <0-180>
        }
    }
}"""

    # Encode the image to base64
    image_base64 = encode_image_to_base64(image_path)

    # API endpoint
    url = 'http://localhost:11434/api/generate'
    # JSON payload
    data = {
        "model": "llava:7b",
        # "model": "Qwen2.5-VL-7B-Instruct",
        "prompt": prompt,
        "images": [image_base64]
    }

    # Send the POST request with stream=True
    start = dt.now()
    response = requests.post(url, json=data, stream=True)
    end = dt.now()
    print(f"Time taken: {end - start}")
    if response.status_code == 200:
        try:
            # Initialize an empty string to collect the model's response
            model_response = ''
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    # Each line is a JSON object
                    json_obj = json.loads(decoded_line)
                    # Append the 'response' field
                    model_response += json_obj.get('response', '')
                    # Check if the 'done' field is True
                    if json_obj.get('done', False):
                        break
            print("Model Response:")
            print(model_response)
        except Exception as e:
            print("Error parsing response:", e)
            # Print the response text for debugging
            print(f"Response text: {response.text}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Error:", response.text)

if __name__ == "__main__":
    main()
