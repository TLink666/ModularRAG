import os
import zipfile

from docx import Document
from docx.oxml.ns import qn

import src.config as config
from src.loaders.image_ocr import image_to_text, valid_ocr


def load_docx(path):

    doc = Document(path)

    image_map = {}

    image_id = 1

    if config.ENABLE_OCR:

        with zipfile.ZipFile(path) as z:

            for name in sorted(z.namelist()):

                if not name.startswith("word/media/"):
                    continue

                image_bytes = z.read(name)

                ocr_text = image_to_text(image_bytes)

                if not valid_ocr(ocr_text):

                    if config.DEBUG:
                        print(f"[OCR] Skip: {repr(ocr_text)}")

                    continue

                image_map[name.split("/")[-1]] = (
                    f"[IMAGE_OCR_{image_id}]\n"
                    f"{ocr_text}\n"
                    f"[/IMAGE_OCR_{image_id}]"
                )

                image_id += 1

    parts = []

    body = doc.element.body

    for child in body:

        # ---------------- Paragraph ----------------
        if child.tag.endswith("p"):

            para = next(
                (p for p in doc.paragraphs if p._element is child),
                None
            )

            if para is not None:

                text = para.text.strip()

                if text:
                    parts.append(text)

            # ---------------- OCR ----------------

            blips = child.findall(".//a:blip", {

                "a":
                "http://schemas.openxmlformats.org/drawingml/2006/main"

            })

            for blip in blips:

                rid = blip.get(
                    qn("r:embed")
                )

                image_part = doc.part.related_parts[rid]

                image_name = os.path.basename(image_part.partname)

                if image_name in image_map:
                    parts.append(image_map[image_name])

    return [{
        "source": os.path.basename(path),
        "page": None,
        "text": "\n\n".join(parts),
        "num_images": len(image_map)
    }]