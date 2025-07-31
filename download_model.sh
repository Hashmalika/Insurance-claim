#!/bin/bash

echo "📥 Downloading phi-3-mini-4k-instruct-q4.gguf from Hugging Face..."

MODEL_DIR="phi3"
mkdir -p $MODEL_DIR

wget -O $MODEL_DIR/phi-3-mini-4k-instruct-q4.gguf \
  https://huggingface.co/malika123/phi3-mini/resolve/main/phi-3-mini-4k-instruct-q4.gguf

echo "✅ Download complete: $MODEL_DIR/phi-3-mini-4k-instruct-q4.gguf"
