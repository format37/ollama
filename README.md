# Local LLM Chat Interface

A simple web interface for interacting with Ollama's LLM models using Gradio. Supports running large language models locally on GPU.

## Features

- Local model execution with Ollama
- Web interface built with Gradio
- Support for multiple Qwen models (7B, 14B, 32B)
- Conversation history management
- JSON response handling
- Example prompts included

## Setup

1. Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start Ollama with desired model:
```bash
./ollama_run.sh  # Default: qwen2.5-coder:32b
```

4. Launch the web interface:
```bash
python ollama_gradio.py
```

Access the chat interface at `http://localhost:7860`

## Files

- `ollama_gradio.py`: Main web interface implementation
- `ollama_run.sh`: Model selection and launch script
- `json_response.py`: Alternative implementation with JSON response handling
- `requirements.txt`: Python dependencies
- `update.sh`: Ollama installation/update script
- `client.py`: Client for interacting with the Ollama server

## Models
A list of available models is published on the [Ollama website](https://ollama.com/models).
To use a different model, modify the `ollama_run.sh` script.