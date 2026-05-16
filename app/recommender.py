import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load data
with open("data.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

# Load FAISS index
index = faiss.read_index("assessment_index.faiss")

model = None


def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def recommend_assessments(query, catalog):
    query = query.lower()

    results = []

    for item in catalog:
        name = item["name"].lower()

        score = 0
        for word in query.split():
            if word in name:
                score += 2

        if score > 0:
            results.append((score, item))

    results.sort(reverse=True, key=lambda x: x[0])

    return [item for _, item in results[:10]]