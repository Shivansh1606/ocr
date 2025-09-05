from flask import Flask, request, jsonify
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ASUS\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

def pdf_to_text_ocr(pdf_path, dpi=300):
    """Convert PDF to text using OCR (Tesseract)."""
    pages = convert_from_path(pdf_path, dpi=dpi)
    full_text = ""
    for i, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page, lang="eng")
        full_text += f"\n\n--- Page {i} ---\n\n{text.strip()}\n"
    return full_text

def image_to_text_ocr(image_path):
    """Convert image to text using OCR (Tesseract)."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang="eng")
    return text.strip()

@app.route("/ocr", methods=["POST"])
def ocr_file():
    """
    API endpoint for OCR extraction.
    Supports both PDF and Image uploads.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename.lower()

    # Save temporarily
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    try:
        if filename.endswith(".pdf"):
            extracted_text = pdf_to_text_ocr(file_path)
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            extracted_text = image_to_text_ocr(file_path)
        else:
            return jsonify({"error": "Unsupported file format. Use PDF, PNG, JPG, or JPEG"}), 400

        return jsonify({"text": extracted_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
