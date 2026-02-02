# System Architecture

## Overview
The system automates social support application processing using an agentic AI architecture with human-in-the-loop governance.

## Core Components
- Frontend: Streamlit (Applicant + Admin UI)
- API Layer: FastAPI
- Agent Orchestration: LangGraph
- ML Models: Scikit-learn
- LLMs: Local (Ollama) + API fallback
- Storage: PostgreSQL + ChromaDB

## Design Principles
- Explainability-first
- Fairness-aware decisioning
- Modular agent responsibilities
- Configurable policy thresholds
- Government-grade auditability
