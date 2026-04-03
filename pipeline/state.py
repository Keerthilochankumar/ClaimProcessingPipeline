from __future__ import annotations
from typing import Any, TypedDict

class State(TypedDict, total=False):
    claim_id: str
    pdf_path: str
    pages_text: dict[int, str]
    pages_images: dict[int, str]
    page_classifications: dict[int, str]
    id_data: dict[str, Any]
    discharge_data: dict[str, Any]
    bill_data: dict[str, Any]
    final_output: dict[str, Any]
    