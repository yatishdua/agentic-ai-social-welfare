# Agentic AI – Social Welfare Eligibility Platform

## Overview

This project implements an **end-to-end Agentic AI–driven Social Welfare Eligibility Platform** designed to automate welfare eligibility assessment, document validation, and post-decision economic enablement. The system reduces manual review time, improves consistency, and enhances applicant experience through explainable and auditable decisioning.

The solution supports **multiple interaction modes** (form-based UI and chatbots) while converging into a **single deterministic decision pipeline** powered by LangGraph.

---

## Problem Statement

Traditional social welfare systems suffer from:

* Manual, slow eligibility review processes
* Inconsistent and subjective decisions
* Poor explainability of outcomes
* Limited guidance for ineligible applicants

This platform addresses these issues by combining **agentic orchestration, deterministic rules, and LLM-powered explainability**.

---

## Key Capabilities

### 1. Multimodal Applicant Intake

Applicants can submit applications through:

* **Form-based UI**
* **Normal LLM Chatbot**
* **Advanced LLM Chatbot**

All inputs (structured data, PDFs, images) are normalized into a common `ApplicationState`, ensuring identical downstream processing regardless of entry path.

---

### 2. Agentic Orchestration with LangGraph

The system uses **LangGraph** to orchestrate specialized agents in a deterministic pipeline:

* **OCR Agent** – Extracts text from bank statements, credit reports, and Emirates ID images
* **Extraction Agent** – LLM-first structured extraction with fallback
* **Validation Agent** – Cross-checks UI inputs against document-derived facts
* **Eligibility Agent** – Applies deterministic eligibility rules
* **Economic Enablement Agent** – Generates recommendations for long-term economic improvement

This separation of concerns ensures modularity, auditability, and reliability.

---

### 3. Deterministic Eligibility Decisioning

Eligibility decisions are **rule-based**, not LLM-driven, ensuring:

* No subjective bias
* Full explainability
* Compliance with policy constraints

Typical criteria include:

* Income thresholds
* Asset limits
* Family size
* Disability considerations

LLMs are never used to approve or reject applications.

---

### 4. Policy Explainability using RAG

For questions such as *“Why am I eligible?”* or *“What are the criteria?”*, the platform uses a **Retrieval-Augmented Generation (RAG)** layer:

* Synthetic policy documents
* Vector store (FAISS)
* Source-cited answers

This RAG layer is **read-only** and does not influence eligibility outcomes.

---

### 5. Economic Enablement Recommendations

Beyond binary eligibility decisions, the platform provides **economic enablement guidance**, such as:

* Job placement assistance
* Upskilling and vocational training suggestions
* Financial planning recommendations
* Disability-specific support programs

This aligns the solution with long-term **economic empowerment**, not just eligibility determination.

---

## High-Level Architecture

### Core Processing Flow

```
Applicant
   │
   ├── Form UI
   ├── Chatbot (Normal LLM)
   └── Chatbot (Advanced LLM)
        │
        ▼
ApplicationState Normalization
        │
        ▼
LangGraph Orchestrator
        │
        ├── OCR Agent
        ├── Extraction Agent
        ├── Validation Agent
        ├── Eligibility Agent
        └── Economic Enablement Agent
        │
        ▼
Final Decision + Recommendations
```

### Explainability Side Channel (RAG)

```
User Question → Policy RAG → Vector Store → Source-Cited Explanation
```

---

## Design Principles

* **One Brain, Many Interfaces** – All interaction modes converge into a single decision pipeline
* **LLMs Assist, Never Decide** – Deterministic logic governs eligibility
* **Auditability by Design** – Every step is traceable via state and logs
* **Enablement over Rejection** – Applicants receive guidance even when ineligible

---

## Outcomes & Benefits

* ⏱️ Decision time reduced from weeks to minutes
* ✅ Consistent and transparent eligibility decisions
* 🤝 Improved applicant experience
* 📊 Fully auditable and extensible architecture
* 🌱 Focus on long-term economic stability

---

## Future Enhancements

* Resume and assets/liabilities document ingestion
* Metadata-filtered policy RAG (e.g., Chroma)
* Session persistence and resume capability
* Advanced analytics and reporting
* API layer (FastAPI) for external integrations

---

## Tech Stack

* **Python**
* **Streamlit** (UI)
* **LangGraph** (agent orchestration)
* **LangChain / OpenAI** (LLM integration)
* **FAISS** (vector store)
* **Tesseract OCR** (document OCR)

---

## Disclaimer

This project uses **synthetic data and documents** for demonstration purposes only. It is intended as a technical case study and not a production welfare system.
