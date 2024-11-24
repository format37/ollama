import gradio as gr
from ollama import Client
import json

# Initialize Ollama client
client = Client()

def chat_with_qwen(message, history):
    # Format the conversation history and new message
    messages = []
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})
    
    # Get response from Ollama
    response = client.chat(
        # model='qwen2.5-coder:7b-instruct',
        model='qwen2.5-coder:32b',
        # model = "llama3.2",
        messages=messages,
        stream=False
    )
    
    return response['message']['content']

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_with_qwen,
    title="NLP assistant",
    description="Chat with Qwen 2.5 Coder model for programming help",
    examples=["Write a Python function to sort a list",
             "Explain how async/await works in JavaScript",
             "Debug this code: print(1+'')",],
    theme=gr.themes.Soft()
)

# Launch the interface
if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0")