import pytesseract
from PIL import Image
import os

class OCREngine:
    @staticmethod
    def extract_text(file_path):
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            return str(e)
