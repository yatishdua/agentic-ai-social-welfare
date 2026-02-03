# Local Setup & Run Guide – Agentic AI Social Welfare Platform

This document provides **step-by-step technical instructions** to run the project locally after cloning the GitHub repository.

---

## 1. System Requirements

Ensure the following are installed:

- **Python**: 3.10 or 3.11 (recommended)
- **Git**
- **Tesseract OCR** (required for document & Emirates ID OCR)
- **OpenAI API Key** (or Azure OpenAI)

> ⚠️ Python 3.12+ is **not recommended** due to dependency incompatibilities.

---

## 2. Clone the Repository

```bash
git clone https://github.com/yatishdua/agentic-ai-social-welfare.git
cd agentic-ai-social-welfare
```

(Optional – chatbot work)
```bash
git checkout feature/multiscreen-chatbot
```

---

## 3. Create & Activate Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` is unavailable:

```bash
pip install streamlit langgraph langchain langchain-openai \
            langchain-community faiss-cpu pydantic \
            pytesseract pillow python-dotenv
```

---

## 5. Install Tesseract OCR

### Windows
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Install (default path recommended)
3. Add to PATH:
   ```
   C:\Program Files\Tesseract-OCR\
   ```

(Optional explicit config in code):
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### macOS
```bash
brew install tesseract
```

### Linux
```bash
sudo apt install tesseract-ocr
```

---

## 6. Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

(Optional – Azure OpenAI)
```env
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=xxx
```

---

## 7. Directory Structure Check

Ensure these directories exist:

```
data/
├── uploads/
├── policy_docs/

src/
├── agents/
├── chatbot_manager/
├── rag/
├── ui/
```

Create if missing:
```bash
mkdir -p data/uploads data/policy_docs
```

---

## 8. Add Policy Documents (Required for RAG)

Place policy documents under:
```
data/policy_docs/
```

Examples:
- `welfare_eligibility_policy.md`
- `welfare_application_process.md`
- `welfare_disability_policy.md`

---

## 9. Run the Application

```bash
streamlit run src/main.py
```

This launches:
- Form-based UI
- Normal chatbot
- Advanced LLM chatbot

All entry paths converge into the same LangGraph pipeline.

---

## 10. Internal Processing Flow

1. User submits application
2. Inputs normalized into `ApplicationState`
3. LangGraph executes:
   - OCR → Extraction → Validation → Eligibility → Enablement
4. Eligibility result is produced
5. Economic enablement recommendations are generated
6. Policy RAG answers explanation queries

---

## 11. Testing All Three Entry Paths

Use identical synthetic inputs to test:
- Form UI
- Normal chatbot
- Advanced chatbot

Expected outcome:
> Identical eligibility and recommendations across all paths.

---

## 12. Common Errors & Fixes

**TesseractNotFoundError**
- Ensure Tesseract is installed and added to PATH

**OpenAI schema / 400 errors**
- Check structured output schemas
- Avoid raw `dict` outputs from LLMs

**Upload UI flicker**
- Ensure chat logic is frozen during upload phase

---

## 13. Production Notes (Out of Scope)

- Dockerize application
- Replace Tesseract with Azure Vision OCR
- Use Chroma / Azure AI Search for RAG
- Persist sessions via Redis or database

---

## Final Note

This repository demonstrates a **case-study-grade, production-inspired architecture** for agentic AI–driven social welfare systems. It is intended for technical evaluation and learning purposes only.

