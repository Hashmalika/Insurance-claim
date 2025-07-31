# import os
# import re
# import json
# from llama_cpp import Llama

# class InsuranceClaimProcessor:
#     def __init__(self, model_path=None):
#         if model_path:
#             self.model_path = os.path.abspath(model_path)
#         else:
#             # Path to the Phi-3 model at project root: ../phi3/phi-3-mini-4k-instruct-q4.gguf
#             base_dir = os.path.dirname(os.path.abspath(__file__))  # app/
#             self.model_path = os.path.abspath(
#                 os.path.join(base_dir, "..", "phi3", "phi-3-mini-4k-instruct-q4.gguf")
#             )

#         print(f"[DEBUG] Final GGUF path: {self.model_path}")
#         self.llm = None
#         self._setup_model()

#     def _setup_model(self):
#         if not os.path.exists(self.model_path):
#             print(f"[ERROR] GGUF model not found at {self.model_path}")
#             return

#         print(f"[INFO] Loading GGUF model from {self.model_path}")
#         # Load with larger context and batch for better stability
#         self.llm = Llama(model_path=self.model_path, n_ctx=4096, n_batch=512)

#     def generate_response(self, prompt: str, max_tokens: int = 512):
#         if self.llm is None:
#             raise ValueError("[ERROR] LLM not initialized")

#         print("[INFO] Running GGUF inference...")
#         response = self.llm(
#             prompt,
#             max_tokens=max_tokens,
#             temperature=0.1,                  # low randomness for consistent JSON
#             stop=["### END_JSON"]              # stop after end marker
#         )

#         raw_output = response["choices"][0]["text"].strip()
#         # Extract JSON between markers
#         match = re.search(r"### START_JSON(.*)", raw_output, re.DOTALL)
#         if match:
#             cleaned = match.group(1).strip()
#         else:
#             cleaned = raw_output

#         # Clean invalid tokens (<, >, or extra 'or')
#         # cleaned = cleaned.replace(" or ", "").replace("<", "").replace(">", "")
#         # Remove stray markers if they exist
#         cleaned = cleaned.replace("### END_JSON", "").strip()


#         # Try to parse JSON safely
#         try:
#             parsed = json.loads(cleaned)
#             return parsed  # return parsed dictionary directly
#         except json.JSONDecodeError:
#             print("[WARNING] Could not parse output as JSON.")
#             print(cleaned)
#             return {}      # return empty dict if parsing fails

# import os
# import re
# import json
# from llama_cpp import Llama

# class InsuranceClaimProcessor:
#     def __init__(self, model_path=None):
#         if model_path:
#             self.model_path = os.path.abspath(model_path)
#         else:
#             # Path to the Phi-3 model at project root: ../phi3/phi-3-mini-4k-instruct-q4.gguf
#             base_dir = os.path.dirname(os.path.abspath(__file__))  # app/
#             self.model_path = os.path.abspath(
#                 os.path.join(base_dir, "..", "phi3", "phi-3-mini-4k-instruct-q4.gguf")
#             )

#         print(f"[DEBUG] Final GGUF path: {self.model_path}")
#         self.llm = None
#         self._setup_model()

#     def _setup_model(self):
#         if not os.path.exists(self.model_path):
#             print(f"[ERROR] GGUF model not found at {self.model_path}")
#             return

#         print(f"[INFO] Loading GGUF model from {self.model_path}")
#         # Load with larger context and batch for better stability
#         self.llm = Llama(model_path=self.model_path, n_ctx=4096, n_batch=512)

#     def _extract_json(self, raw_output: str):
#         """Extract and parse JSON from the raw LLM output."""
#         # Try START_JSON / END_JSON markers
#         match = re.search(r"### START_JSON(.*?)### END_JSON", raw_output, re.DOTALL)
#         if match:
#             cleaned = match.group(1).strip()
#         else:
#             # Fallback: get first JSON block {...}
#             match = re.search(r"(\{.*\})", raw_output, re.DOTALL)
#             if match:
#                 cleaned = match.group(1).strip()
#             else:
#                 print("[WARNING] No JSON markers or blocks found in output.")
#                 return None

#         # Remove any extra markers if they exist
#         cleaned = cleaned.replace("### START_JSON", "").replace("### END_JSON", "").strip()

#         # Parse JSON
#         try:
#             return json.loads(cleaned)
#         except json.JSONDecodeError:
#             print("[WARNING] Could not parse output as JSON.")
#             print("[DEBUG RAW CLEANED OUTPUT]:", cleaned)
#             return None

#     def generate_response(self, prompt: str, max_tokens: int = 512):
#         if self.llm is None:
#             raise ValueError("[ERROR] LLM not initialized")

#         print("[INFO] Running GGUF inference...")
#         response = self.llm(
#             prompt,
#             max_tokens=max_tokens,
#             temperature=0.1,                  # low randomness for consistent JSON
#             stop=["### END_JSON"]              # stop after end marker
#         )

#         raw_output = response["choices"][0]["text"].strip()
#         print("\n[DEBUG RAW MODEL OUTPUT]:\n", raw_output, "\n")  # debug log

#         parsed = self._extract_json(raw_output)

#         if parsed:
#             return parsed
#         else:
#             return {
#                 "error": "Could not parse JSON",
#                 "raw_output": raw_output
#             }


import os
import re
import json
from llama_cpp import Llama
_original_del = Llama.__del__

def safe_del(self):
    try:
        _original_del(self)
    except AttributeError:
        pass

Llama.__del__ = safe_del
from json_repair import repair_json   # <== install: pip install json-repair
from app.download_model import download_file

class InsuranceClaimProcessor:
    def __init__(self, model_path=None):
        if model_path:
            self.model_path = os.path.abspath(model_path)
        else:
            # base_dir = os.path.dirname(os.path.abspath(__file__))  # app/
            # self.model_path = os.path.abspath(
            #     os.path.join(base_dir, "..", "phi3", "phi-3-mini-4k-instruct-q4.gguf")
            # )
            self.model_path = download_file()

        print(f"[DEBUG] Final GGUF path: {self.model_path}")
        self.llm = None
        self._setup_model()

    def _setup_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"[ERROR] GGUF model not found at {self.model_path}")


        print(f"[INFO] Loading GGUF model from {self.model_path}")
        self.llm = Llama(model_path=self.model_path, n_ctx=4096, n_batch=512)

    def _extract_json(self, raw_output: str):
        """Extract and parse JSON from the raw LLM output."""
        # First, try markers
        match = re.search(r"### START_JSON(.*?)### END_JSON", raw_output, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
        else:
            # Fallback: capture first {...}
            match = re.search(r"(\{.*\})", raw_output, re.DOTALL)
            if match:
                cleaned = match.group(1).strip()
            else:
                print("[WARNING] No JSON markers or blocks found in output.")
                return None

        cleaned = cleaned.replace("### START_JSON", "").replace("### END_JSON", "").strip()

        # Attempt normal JSON parse
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            print("[WARNING] JSON malformed. Trying repair...")
            try:
                repaired = repair_json(cleaned)
                return json.loads(repaired)
            except Exception:
                print("[ERROR] JSON could not be repaired.")
                print("[DEBUG CLEANED OUTPUT]:", cleaned)
                return None

    def generate_response(self, prompt: str, max_tokens: int = 700):
        """Run inference and return parsed JSON."""
        if self.llm is None:
            raise ValueError("[ERROR] LLM not initialized")

        print("[INFO] Running GGUF inference...")
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.1,
            stop=["### END_JSON"]
        )

        raw_output = response["choices"][0]["text"].strip()
        print("\n[DEBUG RAW MODEL OUTPUT]\n", raw_output, "\n")

        parsed = self._extract_json(raw_output)

        return parsed if parsed else {
            "error": "Could not parse JSON",
            "raw_output": raw_output
        }
