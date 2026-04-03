
from pipeline.llm import get_chat_model
from pipeline.nodes.build_messages import build_messages
from pipeline.nodes.extract_json import extract_json
from pipeline.state import State
from typing import Any


DISCHARGE_PROMPT = """\
You are an expert medical-insurance data extractor.
Extract the following discharge-summary details from the document.
Return ONLY a JSON object with these keys (use null when a field is not found):

{
  "patient_name": "<string>",
  "admission_date": "<YYYY-MM-DD or null>",
  "discharge_date": "<YYYY-MM-DD or null>",
  "diagnosis": "<string or null>",
  "procedures": ["<string>"],
  "treating_physician": "<string or null>",
  "department": "<string or null>",
  "follow_up_instructions": "<string or null>"
}

Do NOT wrap the JSON in code fences. Do NOT add any explanation.
"""


async def discharge_agent(state: State) -> dict[str, Any]:
    msg = build_messages(state, ["discharge_summary"], DISCHARGE_PROMPT)
    if not msg:
        
        return {"discharge_data": {"message": "No discharge summary pages found"}}

    llm = get_chat_model()
    response = await llm.ainvoke(msg)
    raw = response.content if hasattr(response, "content") else str(response)

    data = extract_json(raw)
    if not data or not isinstance(data, dict):
        data = {"raw_response": raw}

    return {"discharge_data": data}
