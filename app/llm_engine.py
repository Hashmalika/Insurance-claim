# from dotenv import load_dotenv
# import os
# from llama_cpp import Llama
# from sentence_transformers import SentenceTransformer

# # Load environment variables
# load_dotenv()

# # Global variables for LLM and embedding model
# llm = None
# embedding_model = None

# def setup_llm():
#     global llm, embedding_model

#     # Load paths from environment
#     model_path = os.getenv("MODEL_PATH")
#     embedding_model_name = os.getenv("EMBEDDING_MODEL")
  

#     # Print debug info
#     print(f"Loading LLM model from: {model_path}")
#     print(f"Loading embedding model: {embedding_model_name}")

#     # Validate presence of required paths
#     if not model_path or not os.path.exists(model_path):
#         raise ValueError(f"MODEL_PATH not found or invalid: {model_path}")

#     if not embedding_model_name:
#         raise ValueError("EMBEDDING_MODEL not set in environment")

#     # Initialize models
#     llm = Llama(
#         model_path=model_path,
#          n_ctx=512,             # Keep context length small (512 or 1024)
#          n_batch=64,            # Batch size (lower to reduce memory)
#          n_threads=4,           # Match with your CPU cores
#          use_mlock=False,       # Prevent memory lock errors
#          f16_kv=False           # Disable float16 key/value cache
#     )

#     try:
#         embedding_model = SentenceTransformer(embedding_model_name)
#     except Exception as e:
#         raise RuntimeError(f"Failed to load embedding model '{embedding_model_name}': {e}")

#     print("LLM and embedding model loaded successfully.")


import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Initialize once
_embedding_model = SentenceTransformer(EMBEDDING_MODEL)
_llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_gpu_layers=-1)

# ✅ Exported accessors
def get_embedding_model():
    return _embedding_model

def setup_llm():
    return _llm
