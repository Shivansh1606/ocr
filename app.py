from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import pytesseract
import io
from pdf2image import convert_from_bytes

app = Flask(__name__)
CORS(app)  # ✅ ye enable kar dega CORS

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    try:
        text = ""
        if file.filename.lower().endswith(".pdf"):
            pages = convert_from_bytes(file.read(), poppler_path=r"C:\poppler-25.07.0\Library\bin")
            for i, page in enumerate(pages, start=1):
                text += f"\n--- Page {i} ---\n"
                text += pytesseract.image_to_string(page)
        else:
            image = Image.open(file.stream)
            text = pytesseract.image_to_string(image)

        return send_file(
            io.BytesIO(text.encode('utf-8')),
            download_name='converted_text.txt',
            as_attachment=True,
            mimetype='text/plain'
        )
    except Exception as e:
        print("🔥 ERROR:", str(e))
        return f"OCR failed: {str(e)}", 500

if __name__ == '__main__':
    # Host 0.0.0.0 allow external access
    app.run(debug=True, host='0.0.0.0', port=5000)
