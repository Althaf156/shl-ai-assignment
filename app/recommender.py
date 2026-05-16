import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# Load assessment data
with open("data.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("assessment_index.faiss")


def recommend_assessments(user_query):

    # Convert query to embedding
    query_embedding = model.encode([user_query])

    query_embedding = np.array(query_embedding).astype("float32")

    # Search top matches
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