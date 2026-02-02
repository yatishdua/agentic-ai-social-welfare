# Agent Design

## Orchestration
The system uses LangGraph to orchestrate specialized agents with shared state.

## Core Agents
1. Master Orchestrator Agent
2. Chat Interaction Agent
3. Data Ingestion Agent
4. OCR & Multimodal Extraction Agent
5. Data Validation & Conflict Resolution Agent
6. Eligibility Scoring Agent
7. Bias & Fairness Evaluation Agent
8. Decision & Explanation Agent
9. Economic Enablement Recommendation Agent

## Reasoning Framework
- ReAct (Reason → Act → Observe)
- Chain-of-thought stored internally for audit
- User-facing explanations only expose final reasoning
