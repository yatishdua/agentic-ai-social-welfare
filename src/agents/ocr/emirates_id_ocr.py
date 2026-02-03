import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


class OcrEmiratesId:
    """
    OCR processing for Emirates ID cards.
    """

    @staticmethod
    def ocr_emirates_id(image_path: str) -> str:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
