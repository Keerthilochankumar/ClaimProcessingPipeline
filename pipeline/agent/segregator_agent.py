
from typing import Any
from langchain_core.messages import HumanMessage
from pipeline.nodes import extract_pages_content,extract_json
from pipeline.state import State
from pipeline.llm import get_chat_model

DOCUMENT_TYPES = [
    "claim_forms",
    "cheque_or_bank_details",
    "identity_document",
    "itemized_bill",
    "discharge_summary",
    "prescription",
    "investigation_report",
    "cash_receipt",
    "other"
]



SEGREGATOR_PROMPT = """\
You are a medical-claim document classifier. You will receive the content
of one page from an insurance claim PDF (either extracted text or an image).

Your task: classify this page into EXACTLY ONE of these document types:
1. claim_forms          – insurance claim application forms
2. cheque_or_bank_details – bank account or cheque information
3. identity_document    – ID cards, passports, Aadhaar, PAN, or any identity proof
4. itemized_bill        – hospital bills listing charges, line items, costs
5. discharge_summary    – hospital discharge summary with diagnosis, treatment details
6. prescription         – doctor prescriptions for medicines
7. investigation_report – lab reports, diagnostic test results, X-ray reports
8. cash_receipt         – payment receipts, cash memos
9. other                – anything that does not fit the above categories

IMPORTANT: You MUST respond with ONLY this exact JSON format, nothing else:
{{"document_type": "<one_of_the_types_above>"}}
"""



async def segregator_agent(state: State) -> dict[str, Any]:
    pdf_path = state["pdf_path"]
    pages_text, pages_images = extract_pages_content(pdf_path)

    llm = get_chat_model()
    classifications: dict[int, str] = {}

    for idx in range(len(pages_text) + len(pages_images)):
        text = pages_text.get(idx)
        image = pages_images.get(idx)

        content_blocks = [{"type": "text", "text": SEGREGATOR_PROMPT}]
        if text:
            content_blocks.append({"type": "text", "text": f"Page text:\n{text[:4000]}"})
        if image:
            content_blocks.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                }
            )

        msg = [HumanMessage(content=content_blocks)]
        response = await llm.ainvoke(msg)
        raw = response.content if hasattr(response, "content") else str(response)

        parsed = extract_json(raw)
        if parsed and isinstance(parsed, dict):
            doc_type = parsed.get("document_type", "other")
            if doc_type not in DOCUMENT_TYPES:
                doc_type = "other"
        else:
            doc_type = "other"

        classifications[idx] = doc_type
   

    return {
        "pages_text": pages_text,
        "pages_images": pages_images,
        "page_classifications": classifications,
    }

