# models.py
from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    documents: str  # URL to the PDF
    questions: List[str]

class QueryResult(BaseModel):
    question: str
    answer: str
    matched_clauses: List[str]

class QueryResponse(BaseModel):
    results: List[QueryResult]
