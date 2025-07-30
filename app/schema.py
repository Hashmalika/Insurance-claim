from pydantic import BaseModel
from typing import Optional

class EnhancedQuery(BaseModel):
    original_question: str
    age: Optional[int] = None
    medical_condition: Optional[str] = None
    policy_duration: Optional[str] = None
    hospitalization_duration: Optional[str] = None
    treatment_type: Optional[str] = None
