# 🚀 SHL AI Assessment Recommendation System

## 📌 Overview
This project is a FastAPI-based intelligent recommendation system that suggests relevant SHL assessments based on natural language job descriptions. It extracts skill intent (technical and business domains) and ranks assessments using a weighted scoring algorithm.

The system is deployed as a production-ready REST API on Render.

---

## 🎯 Key Features

- 🔍 Natural language understanding of job roles
- ⚖️ Hybrid skill detection (Technical + Finance/Business)
- 📊 Weighted scoring-based recommendation engine
- 🔁 Comparison mode for evaluating two skill domains
- ⚡ Lightweight design optimized for low-memory deployment
- 🌐 Fully deployed REST API (Render)

---

## 🧠 How It Works

1. User sends job description via `/chat` API
2. System extracts keywords from input text
3. Skills are categorized into:
   - Technical (e.g., .NET, backend, API, Python)
   - Business (e.g., accounting, finance, audit)
4. Each assessment is scored using:
   - Keyword matching
   - Domain relevance boosting
   - Cross-skill hybrid scoring
5. Top recommendations are returned

---

## 🏗️ Tech Stack

- Python 3.10+
- FastAPI
- Pydantic
- JSON-based dataset (no heavy ML models for deployment stability)
- Render (deployment platform)

---

## 📡 API Endpoints

### 🔹 Health Check