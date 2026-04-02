from fastapi import FastAPI,File, Form, HTTPException, UploadFile
from dotenv import load_dotenv

app=FastAPI()
load_dotenv()


@app.get("/")
def read_root():
    return {"Hello": "World"}

