import gradio as gr
import requests
import os
import json
import base64
import io
from PIL import Image
import time
import sys

# URL of your LLaVA (or other VLM) inference server
# For example: http://localhost:11434/api/generate
LLAVA_API_URL = os.getenv("LLAVA_API_URL", "http://localhost:11434/api/generate")

def encode_image_to_base64(image):
    """Encodes a PIL Image to a base64 string."""
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

def chat_with_vlm(user_message, image, history):
    """
    Send the user's text prompt + optional image to the VLM inference server.
    Returns the model's answer, generation time, and updates the conversation history.
    """
    if history is None:
        history = []

    start_time = time.time()

    # Optionally build a "prompt" string that includes conversation context
    # For now, let's just use the user's latest message as the "prompt"
    prompt = user_message

    # Base64-encode the image (if provided)
    images_list = []
    if image is not None:
        encoded_img = encode_image_to_base64(image)
        images_list.append(encoded_img)

    # Prepare the JSON payload for your LLaVA (or other) endpoint.
    # Adjust "model" or other fields as needed for your setup:
    data = {
        "model": "llava:7b",
        "prompt": prompt,
        "images": images_list,
    }

    # Post to your local inference endpoint (streaming response)
    # If your endpoint does not use streaming, you'll need to adapt
    # to just read a single JSON response.
    resp = requests.post(LLAVA_API_URL, json=data, stream=True)
    model_response = ""

    try:
        if resp.status_code == 200:
            for line in resp.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    # Each line is a JSON object containing "response" and "done"
                    parsed_json = json.loads(decoded_line)
                    model_response += parsed_json.get("response", "")
                    if parsed_json.get("done", False):
                        break
        else:
            # If the request fails, you can log the error message:
            model_response = f"[Error {resp.status_code}] {resp.text}"

    except Exception as e:
        model_response = f"Error parsing the model response: {e}"

    generation_time = time.time() - start_time

    # Update history
    history.append((user_message, model_response))
    return model_response, generation_time, history

# Now create a Gradio interface with a Textbox + Image input,
# and store the chat history in gr.State
demo = gr.Interface(
    fn=chat_with_vlm,
    inputs=[
        gr.Textbox(label="Message", placeholder="Type your prompt here..."),
        gr.Image(label="Upload Image (optional)", type="pil"),
        gr.State([])  # manages the conversation history
    ],
    outputs=[
        gr.Textbox(label="VLM Response"),
        gr.Number(label="Generation Time (seconds)", precision=2),
        gr.State()  # updated conversation history
    ],
    title="LLaVA Gradio Demo",
    description=(
        "Demo for sending text + optional image to a locally hosted LLaVA (or similar) model. "
        "The model is queried at LLAVA_API_URL (default: http://localhost:11434/api/generate)."
    ),
    examples=[
        ["What's in this image?", None],
        ["What colors can you see?", None]
    ],
    theme=gr.themes.Soft(),
)

if __name__ == "__main__":
    # Force stdout to flush immediately
    sys.stdout.reconfigure(line_buffering=True)
    demo.launch(server_name="0.0.0.0", share=True)