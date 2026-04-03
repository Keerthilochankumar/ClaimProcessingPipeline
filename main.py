from fastapi import FastAPI,File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import uuid
from pathlib import Path

from pipeline.graph import claim_pipeline

load_dotenv()
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE_MB = 40
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)



@app.post("/api/process")
async def process_clame(claim_id: str = Form(...), file: UploadFile = File(...)):
    if file.content_type not in ("application/pdf",):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are allowed.",
        )
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are allowed.",
        )
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded PDF file is empty.")
    safe_name = f"{uuid.uuid4().hex}.pdf"
    pdf_path = UPLOAD_DIR / safe_name
    
    try:
        pdf_path.write_bytes(contents)
        initial_state = {
            "claim_id": claim_id,
            "pdf_path": str(pdf_path.resolve()),
        }
        
        result = await claim_pipeline.ainvoke(initial_state)
        final_output = result.get("final_output", {})
        return JSONResponse(content={"status": "success", "data": final_output})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    

@app.get("/")
def read_root():
    return {"Hello": "World"}

