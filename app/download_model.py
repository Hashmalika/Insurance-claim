import os
import requests
from tqdm import tqdm

def download_file():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_dir = os.path.join(base_dir, "phi3")
    model_path = os.path.join(model_dir, "phi-3-mini-4k-instruct-q4.gguf")

    if os.path.exists(model_path):
        print("✅ Model already exists. Skipping download.")
        return model_path

    os.makedirs(model_dir, exist_ok=True)

    model_url = "https://huggingface.co/malika123/phi3-mini/resolve/main/phi-3-mini-4k-instruct-q4.gguf"
    print("⬇️ Downloading model from Hugging Face...")

    response = requests.get(model_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(model_path, 'wb') as f, tqdm(
        desc="Downloading",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

    print("✅ Download complete.")
    return model_path
