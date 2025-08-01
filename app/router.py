from fastapi import APIRouter, HTTPException
from app.schema import EnhancedQuery
from app.chunker import get_chunks_from_pdf
from app.faiss_index import add_chunks, get_relevant_chunks
from app.prompt import build_prompt
# from app.download_model import download_file
from app.llm_wrapper import InsuranceClaimProcessor
import requests
import os
import tempfile

# download_file()
# Initialize processor once so the model loads only at startup
processor = InsuranceClaimProcessor()

router = APIRouter()

@router.post("/api/v1/hackrx/run")
def process_query(payload: EnhancedQuery):
    try:
         # Handle PDF input (URL or local path)
        if payload.pdf_path.startswith("http"):
            pdf_bytes = requests.get(payload.pdf_path).content
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(pdf_bytes)
                tmp_path = tmp.name
        else:
            if not os.path.exists(payload.pdf_path):
                raise FileNotFoundError(f"PDF not found: {payload.pdf_path}")
            tmp_path = payload.pdf_path
        # Extract chunks and add to FAISS
        chunks = get_chunks_from_pdf(tmp_path)  # Pass path, not bytes
        add_chunks(chunks)

        # Retrieve relevant clauses
        relevant = get_relevant_chunks(payload.query)

        # Build prompt and run Phi-3 inference
        prompt = build_prompt(payload, relevant)
        result_text = processor.generate_response(prompt)

        return {
            "query": payload.query,
            "answer": result_text,
            "clauses": relevant
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
