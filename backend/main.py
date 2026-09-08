from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from detector import analyze_text
from url_analyzer import analyze_url


app = FastAPI(
    title="CyberRakshak API",
    description="AI-powered Cyber Fraud Detection System",
    version="1.0.0"
)


# =========================
# CORS CONFIGURATION
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REQUEST MODELS
# =========================

class TextRequest(BaseModel):
    text: str


class URLRequest(BaseModel):
    url: str


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "project": "CyberRakshak",
        "status": "online",
        "message": "AI Cyber Fraud Detection API is running"
    }


# =========================
# TEXT ANALYSIS
# =========================

@app.post("/analyze/text")
def detect_text(request: TextRequest):

    result = analyze_text(request.text)

    return {
        "type": "text",
        "input": request.text,
        **result
    }


# =========================
# URL ANALYSIS
# =========================

@app.post("/analyze/url")
def detect_url(request: URLRequest):

    result = analyze_url(request.url)

    return {
        "type": "url",
        "input": request.url,
        **result
    }