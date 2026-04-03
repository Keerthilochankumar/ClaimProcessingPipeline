
from typing import Any
from pipeline.llm import get_chat_model
from pipeline.state import State
from pipeline.nodes.build_messages import build_messages
from pipeline.nodes.extract_json import extract_json

BILL_PROMPT = """\
You are an expert medical-insurance data extractor.
Extract ALL line items and costs from the itemized bill pages.
Return ONLY a JSON object with these keys:

{
  "items": [
    {
      "description": "<string>",
      "quantity": <number or null>,
      "unit_price": <number or null>,
      "amount": <number>
    }
  ],
  "subtotal": <number or null>,
  "tax": <number or null>,
  "total_amount": <number>,
  "currency": "<string, e.g. INR or USD>"
}

Do NOT wrap the JSON in code fences. Do NOT add any explanation.
"""



async def bill_agent(state: State) -> dict[str, Any]:
    msg = build_messages(state, ["itemized_bill"], BILL_PROMPT)
    if not msg:
        
        return {"bill_data": {"message": "No itemized bill pages found"}}

    llm = get_chat_model()
    response = await llm.ainvoke(msg)
    raw = response.content if hasattr(response, "content") else str(response)

    data = extract_json(raw)
    if not data or not isinstance(data, dict):
        data = {"raw_response": raw}

    return {"bill_data": data}