import base64
import requests
import json

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

    # Encode the image to base64
    image_base64 = encode_image_to_base64(image_path)

    # API endpoint
    url = 'http://localhost:11434/api/generate'
    # JSON payload
    data = {
        "model": "llava:34b",
        "prompt": prompt,
        "images": [image_base64]
    }

    # Send the POST request with stream=True
    response = requests.post(url, json=data, stream=True)
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
