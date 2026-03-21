import os

from flask import Flask, render_template, request, send_file

from tools.compression import compress_image
from tools.ocr_tool import extract_text
from tools.steganography import decode_text, encode_text

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/encode", methods=["GET", "POST"])
def encode():
    if request.method == "POST":
        image = request.files["image"]
        message = request.form["message"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(filepath)
        output = encode_text(filepath, message)
        return render_template("steg_encode.html", output=output, input_image=filepath)
    return render_template("steg_encode.html", output=None, input_image=None)


@app.route("/decode", methods=["GET", "POST"])
def decode():
    if request.method == "POST":
        image = request.files["image"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(filepath)
        message = decode_text(filepath)
        return render_template("steg_decode.html", message=message, input_image=filepath)
    return render_template("steg_decode.html", message=None, input_image=None)


@app.route("/ocr", methods=["GET", "POST"])
def ocr():
    if request.method == "POST":
        image = request.files["image"]
        lang = request.form.get("lang", "en")
        languages = lang.split(",") if "," in lang else [lang]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(filepath)
        text, results = extract_text(filepath, languages=languages)
        # Pass structured results: list of (text, confidence_percent)
        detections = [(t, round(c * 100, 1)) for (_, t, c) in results if c > 0.1]
        return render_template("ocr.html", text=text, detections=detections, input_image=filepath)
    return render_template("ocr.html", text=None, detections=[])


@app.route("/compress", methods=["GET", "POST"])
def compress():
    if request.method == "POST":
        image = request.files["image"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(filepath)
        output = compress_image(filepath)
        original_size = os.path.getsize(filepath)
        compressed_size = os.path.getsize(output)
        saved_percent = round((1 - compressed_size / original_size) * 100, 1)
        return render_template("compress.html", output=output, input_image=filepath,
                               original_size=round(original_size/1024, 1),
                               compressed_size=round(compressed_size/1024, 1),
                               saved_percent=saved_percent)
    return render_template("compress.html", output=None, input_image=None, original_size=None, compressed_size=None, saved_percent=None)


@app.route("/download")
def download():
    path = request.args.get("path")
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)