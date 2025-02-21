# Ollama Samples

A collection of examples demonstrating how to use Ollama with different models and interfaces.

## Prerequisites

- Docker
- CUDA-capable GPU
- Git

## Quick Start

1. Start the Ollama server:
```bash
sh serve_ollama.sh
```

2. Pull your desired model (e.g., LLaVA):
```bash
sh pull_model.sh llava:7b
```

3. Launch the Gradio interface:
```bash
cd gradio_image
sh run.sh llava:7b
```

4. Open your browser and navigate to: http://0.0.0.0:7860/

## Available Models

You can use various models with this setup. For a complete and up-to-date list of available models, visit [ollama.com/search](https://ollama.com/search).

Some popular vision-language models include:
- llava
- bakllava 
- qwen-vl

And text models like:
- mistral
- codellama
- llama2
- neural-chat
- qwen

## Features

### Image Processing
- Upload and analyze images with LLaVA models
- Real-time image description and analysis
- Support for various image formats

### Text Processing
- Interactive chat interface
- Code generation and analysis
- Support for multiple languages

## Project Structure

- `gradio_image/` - Gradio web interface implementation
- `examples/` - Several examples of using Ollama
- `requirements.txt` - Python dependencies

## Scripts

- `serve_ollama.sh` - Starts the Ollama server with GPU support
- `pull_model.sh` - Downloads specified Ollama models
- `run.sh` - Launches the Gradio interface

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)
