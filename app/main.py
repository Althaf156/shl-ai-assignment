from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.recommender import recommend_assessments
import json

app = FastAPI()

# Load catalog once (SAFE)
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

    conversation_text = ""

    for message in request.messages:
        if message.role == "user":
            conversation_text += " " + message.content

    lower_text = conversation_text.lower()

    blocked_topics = [
        "politics",
        "legal",
        "salary",
        "movie",
        "football",
        "cricket",
        "weather",
        "ignore previous instructions"
    ]

    for topic in blocked_topics:
        if topic in lower_text:
            return {
                "reply": "I can only help with SHL assessment recommendations and comparisons.",
                "recommendations": [],
                "end_of_conversation": False
            }

    # handle short input
    if len(conversation_text.split()) < 3:
        return {
            "reply": "Please provide more details about the role or skills you are hiring for.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # comparison mode
    if "compare" in lower_text:
        matches = recommend_assessments(conversation_text, CATALOG)

        if len(matches) >= 2:
            first = matches[0]
            second = matches[1]

            return {
                "reply": f"{first['name']} focuses on one skill area while {second['name']} evaluates another related competency. Both are useful depending on the requirement.",
                "recommendations": [first, second],
                "end_of_conversation": True
            }

    # normal mode
    recommendations = recommend_assessments(conversation_text, CATALOG)

    if recommendations:
        return {
            "reply": f"Here are some recommended SHL assessments for: {conversation_text}",
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    return {
        "reply": "I could not find matching SHL assessments. Please refine your query.",
        "recommendations": [],
        "end_of_conversation": False
    }