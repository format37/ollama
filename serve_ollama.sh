#!/bin/bash

# Remove existing container
sudo docker rm -f ollama 2>/dev/null

# Then start the main Ollama service
sudo docker run \
  --gpus all \
  --rm \
  --name ollama \
  -v ollama:/root/.ollama \
  -v ./cache:/root/.cache/ \
  --network=host \
  -it ollama/ollama
