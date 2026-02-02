import pdfplumber
from pathlib import Path


class OCRAgent:
    """
    OCR Agent responsible for extracting raw text from documents.
    Currently supports text-based PDFs.
    """

    def extract_text(self, document_path: Path) -> dict:
        
        path = Path(document_path)

        print(f"OCRAgent: Extracting text from {path}")

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError("OCRAgent currently supports only PDF files")

        full_text = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)

        extracted_text = "\n".join(full_text)

        return {
            "text": extracted_text,
            "document_name": path.name,
            "num_pages": len(full_text)
        }
