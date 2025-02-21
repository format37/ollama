#!/bin/bash

# Check if model argument is provided
if [ -z "$1" ]; then
    echo "Error: Model name must be provided"
    echo "Example usage: sh run.sh llava:7b"
    exit 1
fi

# Set model from command line argument
MODEL=$1

# Remove existing container if it exists
sudo docker rm -f ollama-gradio 2>/dev/null || true

# Build the Docker image
sudo docker build -t gradio-app .

# Run the container with environment variable
# --network=host uses host networking mode instead of port mapping
# --rm removes the container when it stops
# --name gives the container a specific name
# -e sets the environment variable for the model
sudo docker run --network=host --rm --name ollama-gradio \
    -e OLLAMA_MODEL="$MODEL" \
    gradio-app
