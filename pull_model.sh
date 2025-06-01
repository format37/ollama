#!/bin/bash

# Check if model argument is provided
if [ -z "$1" ]; then
    echo "Error: Model name must be provided"
    echo "Example usage: sh pull_model.sh llava:7b"
    exit 1
fi

MODEL=$1

# Connect to the existing "ollama" container and pull the specified model
sudo docker exec ollama ollama pull "$MODEL"
