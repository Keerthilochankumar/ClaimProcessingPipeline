
import fitz  
from typing import Tuple
import base64

def extract_node(pdf_path: str) -> Tuple[dict[int, str], dict[int, str]]:
    doc = fitz.open(pdf_path)
    pages_text: dict[int, str] = {}
    pages_images: dict[int, str] = {}
    for i in range(len(doc)):
        page = doc[i]
        text = page.get_text().strip()
        if text:
            pages_text[i] = text
        else:
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("jpeg")
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            pages_images[i] = b64
    doc.close()
    return pages_text, pages_images
