def recommend_assessments(query, catalog):
    query = query.lower()

    scored = []

    for item in catalog:
        name = item["name"].lower()

        score = 0
        for word in query.split():
            if word in name:
                score += 2

        if score > 0:
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [item for _, item in scored[:10]]