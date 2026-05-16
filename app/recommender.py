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


def recommend_assessments(user_query):

    model = get_model()

    query_embedding = model.encode([user_query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, 10)

    recommendations = []

    for idx in indices[0]:
        assessment = assessments[idx]
        recommendations.append({
            "name": assessment["name"],
            "url": assessment["url"],
            "test_type": "General"
        })

    return recommendations