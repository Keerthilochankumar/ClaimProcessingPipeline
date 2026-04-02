from typing import Any
from pipeline.state import State 
from pipeline.nodes import build_messages,extract_json
from pipeline.llm import get_chat_model

ID_AGENT_PROMPT = """\
You are an expert medical-insurance data extractor.
Extract the following identity and policy details from the document.
Return ONLY a JSON object with these keys (use null when a field is not found):

{
  "patient_name": "<string>",
  "date_of_birth": "<YYYY-MM-DD or null>",
  "gender": "<string or null>",
  "id_number": "<string or null>",
  "policy_number": "<string or null>",
  "insurance_provider": "<string or null>",
  "contact_number": "<string or null>",
  "address": "<string or null>"
}

Do NOT wrap the JSON in code fences. Do NOT add any explanation.
"""



async def id_agent(state: State) -> dict[str, Any]:
  
    msg = build_messages(state, ["identity_document", "claim_forms"], ID_AGENT_PROMPT)
    if not msg:
        
        return {"id_data": {"message": "No identity document pages found"}}

    llm = get_chat_model()
    response = await llm.ainvoke(msg)
    raw = response.content if hasattr(response, "content") else str(response)

    data = extract_json(raw)
    if not data or not isinstance(data, dict):
        data = {"raw_response": raw}

    return {"id_data": data}