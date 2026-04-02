from pipeline.state import State
from typing import Any

async def aggregator_node(state: State) -> dict[str, Any]:
    classifications = state.get("page_classifications", {})

    classification_summary: dict[str, list[int]] = {}
    for page_idx, doc_type in classifications.items():
        idx = int(page_idx)
        classification_summary.setdefault(doc_type, []).append(idx + 1)

    final: dict[str, Any] = {
        "claim_id": state.get("claim_id"),
        "document_classification": classification_summary,
        "identity_information": state.get("id_data", {}),
        "discharge_summary": state.get("discharge_data", {}),
        "itemized_bill": state.get("bill_data", {}),
    }

    return {"final_output": final}