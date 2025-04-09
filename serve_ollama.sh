#!/bin/bash

# Remove existing container
sudo docker rm -f ollama 2>/dev/null

# # Then start the main Ollama service
# sudo docker run \
#   --gpus all \
#   --runtime=nvidia \
#   --rm \
#   --name ollama \
#   -v ollama:/root/.ollama \
#   -v ./cache:/root/.cache/ \
#   --network=host \
#   -it ollama/ollama

# Start Ollama targeting ONLY GPU 0 (likely the 4090)
sudo docker run \
  -e CUDA_VISIBLE_DEVICES=0 \
  --gpus all \
  --runtime=nvidia \
  --rm \
  --name ollama \
  -v ollama:/root/.ollama \
  -v ./cache:/root/.cache/ \
  --network=host \
  -it ollama/ollama