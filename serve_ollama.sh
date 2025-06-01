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

# To decrease the GPU power if GPU is broken:
# sudo nvidia-smi -pl 125

# NORMAL RUN
sudo docker run \
  -d \
  -e CUDA_VISIBLE_DEVICES=0 \
  --gpus all \
  --runtime=nvidia \
  --rm \
  --name ollama \
  -v ollama:/root/.ollama \
  -v ./cache:/root/.cache/ \
  --network=host \
  -it ollama/ollama

# # BROKEN GPU
# sudo docker run \
#   -e CUDA_VISIBLE_DEVICES=1 \
#   --gpus all \
#   --runtime=nvidia \
#   --rm \
#   --name ollama \
#   -v ollama:/root/.ollama \
#   -v ./cache:/root/.cache/ \
#   --network=host \
#   -it --entrypoint /bin/bash ollama/ollama
