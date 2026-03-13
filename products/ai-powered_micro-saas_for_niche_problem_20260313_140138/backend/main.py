from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="AI-Powered Micro-SaaS for Niche Problem API")

@app.get("/")
def read_root():
    return {"status": "online", "name": "AI-Powered Micro-SaaS for Niche Problem"}

@app.get("/api/features")
def get_features():
    return []

@app.get("/health")
def health():
    return {"status": "healthy"}
