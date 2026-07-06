import os
import fitz

import src.config as config
from src.loaders.image_ocr import image_to_text, valid_ocr


def load_pdf(path):

    pdf = fitz.open(path)

    pages = []

    for page_idx in range(len(pdf)):

        page = pdf.load_page(page_idx)

        blocks = page.get_text("dict")["blocks"]

        full_text = []

        image_count = 0

        for block in blocks:

            # ---------- Text Block ----------
            if block["type"] == 0:

                lines = []

                for line in block["lines"]:
                    spans = [
                        span["text"]
                        for span in line["spans"]
                    ]
                    lines.append("".join(spans))

                text = "\n".join(lines).strip()

                if text:
                    full_text.append(text)

            # ---------- Image Block ----------
            elif block["type"] == 1 and config.ENABLE_OCR:

                try:
                    xref = block["xref"]

                    base_image = pdf.extract_image(xref)

                    image_bytes = base_image["image"]

                    ocr_text = image_to_text(image_bytes)

                    if not valid_ocr(ocr_text):

                        if config.DEBUG:
                            print(f"[OCR] Skip: {repr(ocr_text)}")

                        continue

                    image_count += 1

                    full_text.append(
                        f"[IMAGE_OCR_{page_idx+1}_{image_count}]\n"
                        f"{ocr_text}\n"
                        f"[/IMAGE_OCR_{page_idx+1}_{image_count}]"
                    )

                except Exception as e:

                    if config.DEBUG:
                        print(e)

        pages.append({

            "source": os.path.basename(path),

            "page": page_idx + 1,

            "text": "\n\n".join(full_text),

            "num_images": image_count

        })

    pdf.close()

    return pages