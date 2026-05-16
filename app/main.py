from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.recommender import recommend_assessments
import json

app = FastAPI()

with open("data.json", "r", encoding="utf-8") as f:
    CATALOG = json.load(f)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):

    conversation_text = " ".join(
        [m.content for m in request.messages if m.role == "user"]
    )

    lower_text = conversation_text.lower()

    if len(conversation_text.split()) < 3:
        return {
            "reply": "Please provide more details about the role or skills.",
            "recommendations": [],
            "end_of_conversation": False
        }

    if "compare" in lower_text:
        matches = recommend_assessments(conversation_text, CATALOG)

        if len(matches) >= 2:
            return {
                "reply": f"{matches[0]['name']} vs {matches[1]['name']}",
                "recommendations": matches[:2],
                "end_of_conversation": True
            }

    recommendations = recommend_assessments(conversation_text, CATALOG)

    return {
        "reply": f"Here are recommendations for: {conversation_text}",
        "recommendations": recommendations,
        "end_of_conversation": True
    }