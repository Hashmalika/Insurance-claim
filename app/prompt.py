# from app.schema import EnhancedQuery
# from typing import List, Dict

# def build_prompt(enhanced_query: EnhancedQuery, relevant_clauses: List[Dict]) -> str:
#     clause_text = "\n".join(f"- {c}" for c in relevant_clauses)

#     prompt = f"""
# You are an expert insurance claim analyst.

# Analyze the user query and relevant policy clauses. Return the decision **strictly as JSON** between the markers.

# ## Query Info:
# - Question: {enhanced_query.original_question}
# - Age: {enhanced_query.age}
# - Medical Condition: {enhanced_query.medical_condition}
# - Treatment Type: {enhanced_query.treatment_type}
# - Hospitalization Duration: {enhanced_query.hospitalization_duration}
# - Policy Duration: {enhanced_query.policy_duration}

# ## Relevant Policy Clauses:
# {clause_text}

# ## Output Format:
# Return your answer **between the following markers**:

# ### START_JSON
# {{
#   "decision": "approved" or "rejected" or "needs_more_info",
#   "amount": a number if applicable or null,
#   "justification": "clear explanation using the clauses above",
#   "matched_clauses": [
#     {{
#       "clause_id": "exact clause number if available",
#       "clause_text": "exact clause text that supports the decision"
#     }}
#   ]
# }}
# ### END_JSON

# Do not write anything outside START_JSON and END_JSON.
# """
#     return prompt.strip()


# from app.schema import EnhancedQuery
# from typing import List, Dict

# def build_prompt(enhanced_query: EnhancedQuery, relevant_clauses: List[Dict]) -> str:
#     clause_text = "\n\n".join(f"- {c}" for c in relevant_clauses)

#     prompt = f"""
# You are an insurance claim analyst. Use the query & clauses to decide coverage.

# ## Query:
# {enhanced_query.original_question}
# Age: {enhanced_query.age}, Condition: {enhanced_query.medical_condition}, 
# Treatment: {enhanced_query.treatment_type}, Hosp: {enhanced_query.hospitalization_duration}, 
# Policy: {enhanced_query.policy_duration}

# ## Clauses:
# {clause_text}

# ### START_JSON
# {{
#   "decision": "approved/rejected/needs_more_info",
#   "amount": <number or null>,
#   "justification": "reason based only on clauses",
#   "matched_clauses": [
#     {{"clause_id": "<id>", "clause_text": "<text>"}}
#   ],
#   "query_info": {{
#     "age": <int or null>,
#     "medical_condition": "<string>",
#     "treatment_type": "<string>",
#     "hospitalization_duration": "<string>",
#     "policy_duration": "<string>"
#   }}
# }}
# ### END_JSON
# """.strip()

#     return prompt


# from app.schema import EnhancedQuery
# from typing import List, Dict

# def build_prompt(enhanced_query: EnhancedQuery, relevant_clauses: List[Dict]) -> str:
#     clause_text = "\n\n".join(f"- {c}" for c in relevant_clauses)

#     prompt = f"""
# You are an insurance claim analyst. Use the query & clauses to decide coverage.

# ## Query:
# {enhanced_query.original_question}
# Age: {enhanced_query.age}, Condition: {enhanced_query.medical_condition}, 
# Treatment: {enhanced_query.treatment_type}, Hosp: {enhanced_query.hospitalization_duration}, 
# Policy: {enhanced_query.policy_duration}

# ## Clauses:
# {clause_text}

# ### START_JSON
# {{
#   "decision": "approved/rejected/needs_more_info",
#   "amount": "₹<amount or null>",
#   "justification": "short reason based only on clauses",
#   "matched_clauses": [
#     {{
#       "clause_id": "id or null",
#       "clause_text": "exact clause text or empty"
#     }}
#   ],
#   "query_info": {{
#     "age": {enhanced_query.age if enhanced_query.age else "null"},
#     "medical_condition": "{enhanced_query.medical_condition or 'needs_more_info'}",
#     "treatment_type": "{enhanced_query.treatment_type or 'needs_more_info'}",
#     "hospitalization_duration": "{enhanced_query.hospitalization_duration or 'needs_more_info'}",
#     "policy_duration": "{enhanced_query.policy_duration or 'needs_more_info'}"
#   }}
# }}
# ### END_JSON
# """.strip()

from app.schema import EnhancedQuery
from typing import List, Dict

def build_prompt(enhanced_query: EnhancedQuery, relevant_clauses: List[Dict]) -> str:
    clause_text = "\n\n".join(f"- {c}" for c in relevant_clauses)

    prompt = f"""
You are an insurance claim analyst. Based on the query and clauses, return ONLY a JSON object. 
Do NOT add explanations outside the JSON. Wrap the JSON between ### START_JSON and ### END_JSON.

## Query:
{enhanced_query.original_question}
Age: {enhanced_query.age}, Condition: {enhanced_query.medical_condition},
Treatment: {enhanced_query.treatment_type}, Hosp: {enhanced_query.hospitalization_duration},
Policy: {enhanced_query.policy_duration}

## Relevant Clauses:
{clause_text}

### START_JSON
{{
  "decision": "approved",
  "amount": "₹1,80,000",
  "justification": "Treatment is covered as per policy clauses and hospitalization criteria is met.",
  "matched_clauses": [
    {{
      "clause_id": "CL-01",
      "clause_text": "Fracture treatment is covered up to the sum insured."
    }}
  ],
  "query_info": {{
    "age": 30,
    "medical_condition": "fracture treatment",
    "treatment_type": "surgery",
    "hospitalization_duration": "5 days",
    "policy_duration": "3 years"
  }}
}}
### END_JSON

Now return the JSON for the current query in the SAME format, 
wrapped inside ### START_JSON and ### END_JSON. Do NOT add anything else.
### START_JSON
""".strip()

    return prompt
