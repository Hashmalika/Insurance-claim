import pdfplumber
import os
import requests
from io import BytesIO

def get_chunks_from_pdf(pdf_path_or_url, max_len=250):
    """
    Extracts text from a PDF (local or URL), splits it into word chunks of max_len size.
    Returns a list of text chunks.
    """
    # Handle URL or local path
    if pdf_path_or_url.startswith("http://") or pdf_path_or_url.startswith("https://"):
        try:
            response = requests.get(pdf_path_or_url)
            response.raise_for_status()
            pdf_file = BytesIO(response.content)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to download PDF from URL: {e}")
    else:
        if not os.path.exists(pdf_path_or_url):
            raise FileNotFoundError(f"PDF not found at: {os.path.abspath(pdf_path_or_url)}")
        pdf_file = pdf_path_or_url

    # Extract text from PDF
    try:
        with pdfplumber.open(pdf_file) as pdf:
            all_text = []
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    print(f"[Warning] Page {i+1} has no extractable text.")
                    continue
                all_text.append(text.strip())

        full_text = " ".join(all_text).strip()

        if not full_text:
            raise ValueError("No extractable text found in PDF.")

        # Split into word chunks
        words = full_text.split()
        return [" ".join(words[i:i + max_len]) for i in range(0, len(words), max_len)]

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")
