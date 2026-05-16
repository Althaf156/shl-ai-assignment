# SHL AI Assessment Recommendation System

## Overview

This project is an AI-powered recommendation system for SHL assessments.

It supports:
- conversational assessment recommendations
- semantic search using embeddings
- assessment comparison
- stateless chat interactions
- prompt injection protection

The system uses FastAPI as the backend and FAISS vector search for semantic retrieval.

---

## Features

### 1. Conversational Recommendations
Users can provide hiring requirements in natural language.

Example:
- "Hiring a .NET developer with accounting skills"

The system returns relevant SHL assessments.

---

### 2. Semantic Search
The project uses:
- sentence-transformers
- FAISS vector indexing

to retrieve semantically relevant assessments.

---

### 3. Comparison Support
Users can compare assessments.

Example:
- "Compare .NET Framework and ADO.NET assessments"

---

### 4. Guardrails
The system rejects:
- off-topic questions
- prompt injection attempts

---

## Tech Stack

- Python
- FastAPI
- FAISS
- Sentence Transformers
- Selenium
- BeautifulSoup

---

## API Endpoints

### Health Check

GET /health

---

### Chat Endpoint

POST /chat

Example request:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring backend software engineer with finance knowledge"
    }
  ]
}