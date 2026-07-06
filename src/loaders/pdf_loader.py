import os
import fitz
from pypdf import PdfReader

import src.config as config
from src.loaders.image_ocr import image_to_text, valid_ocr


def extract_pdf_images_ocr(pdf, page_idx, source, page_num):
    image_blocks = []
    image_list = pdf.load_page(page_idx).get_images(full=True)

    image_id = 1

    for img in image_list:
        xref = img[0]
        base_image = pdf.extract_image(xref)
        image_bytes = base_image["image"]

        ocr_text = image_to_text(image_bytes)

        if not valid_ocr(ocr_text):
            if config.DEBUG:
                print(f"[OCR] Skip: {repr(ocr_text)}")
            continue

        image_blocks.append(
            f"\n[IMAGE_{page_num}_{image_id}]\n"
            f"{ocr_text}\n"
            f"[/IMAGE_{page_num}_{image_id}]"
        )

        image_id += 1

    return image_blocks


def load_pdf(path):

    reader = PdfReader(path)
    pdf = fitz.open(path)

    pages = []

    for page_idx, page in enumerate(reader.pages, start=0):

        page_text = page.extract_text() or ""
        full_text = page_text

        image_blocks = []

        if config.ENABLE_OCR:
            image_blocks = extract_pdf_images_ocr(
                pdf,
                page_idx,
                os.path.basename(path),
                page_idx + 1
            )

        if image_blocks:
            full_text += "\n\n" + "\n\n".join(image_blocks)

        pages.append({
            "source": os.path.basename(path),
            "page": page_idx + 1,
            "text": full_text,
            "num_images": len(image_blocks)
        })

    pdf.close()
    return pages