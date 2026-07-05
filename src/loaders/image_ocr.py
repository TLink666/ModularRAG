from pypdf import PdfReader
from src.config import ENABLE_OCR, OCR_MIN_LENGTH, OCR_MIN_LETTERS, TESSERACT
import os
import fitz  # pymupdf
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = TESSERACT

MIN_OCR_LENGTH = 20

def image_to_text(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))

    # 转灰度
    image = image.convert("L")

    # 放大，提高 OCR 精度
    # image = image.resize(
    #     (image.width * 2, image.height * 2)
    # )

    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text.strip()

def valid_ocr(text):
    """
    Filter obviously noisy OCR results.
    """

    text = text.strip()

    if not text:
        return False

    letters = sum(c.isalpha() for c in text)

    words = len(text.split())

    if letters < OCR_MIN_LETTERS:
        return False

    if len(text) < OCR_MIN_LENGTH and words < 2:
        return False

    return True