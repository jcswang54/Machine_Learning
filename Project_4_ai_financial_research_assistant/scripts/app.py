from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.pipeline import research

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "NVIDIA Financial Research Assistant API"}

@app.post("/research")
def research_endpoint(request: ResearchRequest):
    answer, sources = research(request.query)

    return {
        "answer": answer,
        "sources": sources
    }