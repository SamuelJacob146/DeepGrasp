from fastapi import FastAPI, Request, UploadFile, File
from pydantic import BaseModel
import os
from pdf_utils import extract_text_from_pdf
from fastapi.responses import JSONResponse

app = FastAPI()

class Question(BaseModel):
    query: str

UPLOAD_DIR = "data/sample_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported"})

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_location)
    
    # Save text temporarily for inspection
    with open(file_location + ".txt", "w") as f:
        f.write(text)

    return {
        "filename": file.filename,
        "extracted_characters": len(text),
        "preview": text[:500]
    }



@app.get("/")
def root():
    return {"message": "Welcome to DeepGrasp"}

@app.post("/ask")
async def ask_question(question: Question):
    return {
        "query": question.query,
        "answer": "This is a placeholder answer. RAG will go here later!"
    }
