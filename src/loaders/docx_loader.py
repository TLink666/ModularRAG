import io
import os
import zipfile

from docx import Document
import src.config as config
from src.loaders.image_ocr import image_to_text, valid_ocr


def load_docx(path):

    doc = Document(path)

    paragraphs = [
        p.text
        for p in doc.paragraphs
        if p.text.strip()
    ]

    image_blocks = []

    if config.ENABLE_OCR:

        with zipfile.ZipFile(path) as z:

            image_id = 1

            for name in z.namelist():

                if not name.startswith("word/media/"):
                    continue
                image_bytes = z.read(name)
                image_bytes = z.read(name)

                ocr_text = image_to_text(image_bytes)

                if not valid_ocr(ocr_text):
                    if config.DEBUG:
                        print(f"[OCR] Skip: {repr(ocr_text)}")
                    continue
                    

                image_blocks.append(
                    f"\n[IMAGE_{image_id}]\n"
                    f"{ocr_text}\n"
                    f"[/IMAGE_{image_id}]"
                )

                image_id += 1

    text = "\n".join(paragraphs)

    if image_blocks:
        text += "\n\n" + "\n\n".join(image_blocks)

    return [{
        "source": os.path.basename(path),
        "page": None,
        "text": text,
        "num_images": len(image_blocks)
    }]