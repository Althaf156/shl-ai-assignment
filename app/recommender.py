import json

# Load once (LIGHTWEIGHT — SAFE FOR RENDER)
with open("data.json", "r", encoding="utf-8") as f:
    CATALOG = json.load(f)


TECH_KEYWORDS = [
    "net", "dotnet", ".net", "backend", "api", "microservices",
    "java", "python", "django", "flask", "sql"
]

BUSINESS_KEYWORDS = [
    "accounting", "finance", "audit", "bookkeeping", "tax"
]


def recommend_assessments(query: str, catalog=None):
    query = query.lower()
    catalog = catalog or CATALOG

    results = []

    for item in catalog:
        name = item.get("name", "").lower()

        score = 0

        # Base keyword matching
        for word in query.split():
            if word in name:
                score += 2

        # 🔥 TECH BOOST
        if any(t in query for t in TECH_KEYWORDS) and any(t in name for t in TECH_KEYWORDS):
            score += 5

        # 🔥 BUSINESS BOOST
        if any(b in query for b in BUSINESS_KEYWORDS) and any(b in name for b in BUSINESS_KEYWORDS):
            score += 4

        # 🔥 CROSS SIGNAL (important for SHL matching quality)
        if "net" in query and ".net" in name:
            score += 6

        if "account" in query and ("account" in name or "finance" in name):
            score += 4

        if score > 0:
            results.append((score, item))

    # sort best matches first
    results.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in results[:10]]