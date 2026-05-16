from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.recommender import recommend_assessments
import os
import json

app = FastAPI()

# -----------------------------
# SAFE CATALOG LOADING
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    CATALOG = json.load(f)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/")
def root():
    return {"status": "SHL AI API running"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):

    # -----------------------------
    # BUILD USER CONTEXT
    # -----------------------------
    conversation_text = " ".join(
        m.content for m in request.messages if m.role == "user"
    ).strip()

    if not conversation_text:
        return {
            "reply": "Please provide a valid job role description.",
            "recommendations": [],
            "end_of_conversation": False
        }

    lower_text = conversation_text.lower()

    # -----------------------------
    # BLOCKED TOPICS SAFETY LAYER
    # -----------------------------
    blocked_topics = [
        "politics", "legal", "salary", "movie",
        "football", "cricket", "weather",
        "ignore previous instructions"
    ]

    if any(topic in lower_text for topic in blocked_topics):
        return {
            "reply": "I only assist with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # GET RECOMMENDATIONS (SAFE CALL)
    # -----------------------------
    try:
        recommendations = recommend_assessments(conversation_text, CATALOG)
    except Exception as e:
        return {
            "reply": "Error while processing recommendation logic.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # SHORT INPUT HANDLING
    # -----------------------------
    if len(conversation_text.split()) < 3:
        return {
            "reply": "Please provide more details about the role or skills.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # COMPARE MODE
    # -----------------------------
    if "compare" in lower_text and len(recommendations) >= 2:
        first, second = recommendations[:2]

        return {
            "reply": f"{first['name']} vs {second['name']} comparison based on skills match.",
            "recommendations": [first, second],
            "end_of_conversation": True
        }

    # -----------------------------
    # NORMAL RESPONSE
    # -----------------------------
    return {
        "reply": f"Here are recommended SHL assessments for: {conversation_text}",
        "recommendations": recommendations[:10],
        "end_of_conversation": True
    }