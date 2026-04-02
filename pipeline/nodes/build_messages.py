from langchain_core.messages import HumanMessage
from pipeline.state import State
def build_messages(
    state: State,
    target_types: list[str],
    system_prompt: str,
) -> list[HumanMessage] | None:
    classifications = state.get("page_classifications", {})
    pages_text = state.get("pages_text", {})
    pages_images = state.get("pages_images", {})

    content_blocks = [{"type": "text", "text": system_prompt + "\n\nDocument details below:\n"}]
    found_any = False
    for page_idx, doc_type in classifications.items():
        idx = int(page_idx)
        if doc_type in target_types:
            found_any = True
            text = pages_text.get(idx, pages_text.get(str(idx), ""))
            image = pages_images.get(idx, pages_images.get(str(idx), ""))

            content_blocks.append({"type": "text", "text": f"\n--- PAGE {idx + 1} ---\n"})
            if text:
                content_blocks.append({"type": "text", "text": text})
            if image:
                content_blocks.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                    }
                )

    if not found_any:
        return None
    
    return [HumanMessage(content=content_blocks)]