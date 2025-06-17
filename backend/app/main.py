from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Welcome to DeepGrasp"}

@app.post("/ask")
async def ask_question(question: Question):
    return {
        "query": question.query,
        "answer": "This is a placeholder answer. RAG will go here later!"
    }
