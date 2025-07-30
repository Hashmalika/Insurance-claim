import asyncio
import re
import os
import json
from app.chunker import get_chunks_from_pdf
from app.faiss_index import add_chunks, get_relevant_chunks
from app.prompt import build_prompt
from app.schema import EnhancedQuery
from app.llm_wrapper import InsuranceClaimProcessor

# === CONFIGURATION (absolute paths) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # directory of test.py
PDF_PATH = os.path.join(BASE_DIR, "app", "static", "sample_policy.pdf")

USER_QUERY = "Hospitalized for 3 days for cataract surgery. Policy active for 2 years. Coverage is ₹1,00,000."


# === QUERY PARSING ===
def extract_fields_from_query(query: str) -> EnhancedQuery:
    age_match = re.search(r'(\d+)\s*years? old', query, re.IGNORECASE)
    duration_match = re.search(r'(\d+\s*(year|month|day)s?) policy', query, re.IGNORECASE)
    hospitalization_match = re.search(r'(\d+)\s*days? of hospitalization', query, re.IGNORECASE)
    condition_match = re.search(r'underwent (.+?) (treatment|procedure|surgery|operation)?', query, re.IGNORECASE)
    treatment_type_match = re.search(r'underwent .+? (surgery|consultation|treatment|procedure)', query, re.IGNORECASE)

    return EnhancedQuery(
        original_question=query,
        age=int(age_match.group(1)) if age_match else None,
        medical_condition=condition_match.group(1).strip() if condition_match else "unspecified",
        policy_duration=duration_match.group(1).strip() if duration_match else "unspecified",
        hospitalization_duration=hospitalization_match.group(1).strip() + " days" if hospitalization_match else "unspecified",
        treatment_type=treatment_type_match.group(1).strip() if treatment_type_match else "unspecified"
    )

# === TEST EXECUTION ===
async def run_test():
    # Check if PDF exists
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"[ERROR] PDF not found at: {PDF_PATH}")

    print(f"[INFO] Extracting chunks from: {PDF_PATH}")
    chunks = get_chunks_from_pdf(PDF_PATH)
    print(f"[INFO] Total Chunks Extracted: {len(chunks)}")

    add_chunks(chunks)

    print(f"\n[INFO] Processing query: {USER_QUERY}")
    enhanced_query = extract_fields_from_query(USER_QUERY)
    print(f"[DEBUG] Parsed Query: {enhanced_query.dict()}")

    relevant_chunks = get_relevant_chunks(enhanced_query.original_question, top_k=3)
    print(f"[DEBUG] Relevant Chunks Found: {len(relevant_chunks)}")

    prompt = build_prompt(enhanced_query, relevant_chunks)

    # Initialize LLM
    processor = InsuranceClaimProcessor()

    if processor.llm is None:
        print(f"[ERROR] GGUF model not loaded. Check model path in llm_wrapper.py")
        return  # Stop gracefully instead of raising exception

    print("\n[INFO] Running LLM inference...")
    try:
        parsed_output = processor.generate_response(prompt=prompt, max_tokens=700)
    except Exception as e:
        print(f"[ERROR] LLM inference failed: {e}")
        return

    print("\n[LLM RAW RESPONSE]")
    # Show raw JSON string if parsed successfully, else the cleaned text
    if isinstance(parsed_output, dict):
        # Reconstruct the raw JSON for clarity
        print(json.dumps(parsed_output, indent=2, ensure_ascii=False))
    else:
        print(parsed_output)

    print("\n[PARSED OUTPUT]")
    if isinstance(parsed_output, dict) and parsed_output:
        print(json.dumps(parsed_output, indent=2, ensure_ascii=False))
    else:
        print("[WARNING] Could not parse output as JSON. Check model's response formatting.")

if __name__ == "__main__":
    asyncio.run(run_test())
