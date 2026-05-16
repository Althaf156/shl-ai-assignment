import json

# Load catalog once
with open("data.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def recommend_assessments(query, catalog):

    query = query.lower()

    tech_keywords = ["net", "java", "python", "backend", "api"]
    business_keywords = ["accounting", "finance", "audit"]

    results = []

    for item in catalog:
        name = item["name"].lower()

        score = 0

        # ----------------------------
        # BASIC WORD MATCHING
        # ----------------------------
        for word in query.split():
            if word in name:
                score += 2

        # ----------------------------
        # TECH SKILL BOOST
        # ----------------------------
        if any(tech in query for tech in tech_keywords) and any(tech in name for tech in tech_keywords):
            score += 5

        # ----------------------------
        # BUSINESS SKILL BOOST
        # ----------------------------
        if any(biz in query for biz in business_keywords) and any(biz in name for biz in business_keywords):
            score += 4

        # ----------------------------
        # SPECIAL CASE BOOST (your rule)
        # ----------------------------
        if "net" in name:
            score += 5

        if "account" in name or "finance" in name:
            score += 4

        # store only relevant results
        if score > 0:
            results.append((score, item))

    # sort best match first
    results.sort(reverse=True, key=lambda x: x[0])

    return [item for _, item in results[:10]]