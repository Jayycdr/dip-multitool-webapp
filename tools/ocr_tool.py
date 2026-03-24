# ocr.py — Replit-safe OCR using doctr (pure Python, no system Tesseract needed)
# Install: pip install python-doctr[torch]
#
_model = None

def get_model():
    global _model
    if _model is None:
        from doctr.models import ocr_predictor
        _model = ocr_predictor(pretrained=True)
    return _model

def extract_text(image_path, languages=None):
    """
    Extract text from an image using doctr.
    Returns (full_text: str, results: list of dicts with text + confidence).
    Drop-in replacement for the EasyOCR version.
    """
    from doctr.io import DocumentFile

    model = get_model()
    doc = DocumentFile.from_images(image_path)
    output = model(doc)

    lines = []
    results = []

    for page in output.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    confidence = word.confidence
                    text = word.value
                    if confidence > 0.1:
                        lines.append(text)
                        results.append({
                            "text": text,
                            "confidence": confidence,
                            "geometry": word.geometry  # ((x1,y1),(x2,y2)) relative coords
                        })

    full_text = " ".join(lines)
    return full_text, results
