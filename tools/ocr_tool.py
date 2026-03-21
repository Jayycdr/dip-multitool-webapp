import easyocr

# Reader is initialized once and reused (loading is slow, inference is fast)
# lang_list can be extended e.g. ['en', 'hi'] for Hindi+English
_reader = None


def get_reader(languages=None):
    global _reader
    if languages is None:
        languages = ['en']
    if _reader is None:
        _reader = easyocr.Reader(languages, gpu=False)
    return _reader


def extract_text(image_path, languages=None):
    """
    Extract text from an image using EasyOCR.
    Returns a plain string with all detected text joined by newlines.
    Also returns structured results for confidence display.
    """
    reader = get_reader(languages)
    results = reader.readtext(image_path)

    # results is a list of (bbox, text, confidence)
    lines = [text for (_, text, confidence) in results if confidence > 0.1]
    full_text = "\n".join(lines)

    return full_text, results