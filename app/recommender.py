def recommend_assessments(query, catalog):
    query = query.lower()

    tech_keywords = ["net", "java", "python", "backend", "api"]
    business_keywords = ["accounting", "finance", "audit"]

    results = []

    for item in catalog:
        name = item["name"].lower()

        score = 0

        # base match
        for word in query.split():
            if word in name:
                score += 2

        # skill boosting
        if "net" in query or "dotnet" in query:
            if "net" in name:
                score += 5

        if any(k in query for k in business_keywords):
            if any(k in name for k in business_keywords):
                score += 4

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in results[:10]]