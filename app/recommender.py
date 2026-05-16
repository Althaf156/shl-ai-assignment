def recommend_assessments(query: str, catalog):
    query = query.lower()

    tech_keywords = ["net", "dotnet", "backend", "api", "java", "python"]
    finance_keywords = ["accounting", "finance", "audit", "bookkeeping"]

    results = []

    for item in catalog:
        name = item["name"].lower()
        score = 0

        # base match
        for word in query.split():
            if word in name:
                score += 2

        # tech boost
        if any(t in query for t in tech_keywords) and any(t in name for t in tech_keywords):
            score += 5

        # finance boost
        if any(f in query for f in finance_keywords) and any(f in name for f in finance_keywords):
            score += 5

        # hybrid boost (very important for SHL case)
        if any(t in name for t in tech_keywords) and any(f in name for f in finance_keywords):
            score += 3

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)

    return [item for _, item in results[:10]]