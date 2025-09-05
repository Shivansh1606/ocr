from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os

# Set path to Tesseract OCR executable (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ASUS\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_text_from_file(file_path, dpi=300):
    """
    Extract text from a single PDF or image file.
    """
    full_text = ""
    try:
        if file_path.lower().endswith(".pdf"):
            # Convert PDF to images
            pages = convert_from_path(file_path, dpi=dpi)
            for page_number, page_image in enumerate(pages, start=1):
                text = pytesseract.image_to_string(page_image, lang="eng")
                full_text += f"\n\n--- {os.path.basename(file_path)} | Page {page_number} ---\n\n{text.strip()}\n"
        else:
            # Image file
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang="eng")
            full_text += f"\n\n--- {os.path.basename(file_path)} ---\n\n{text.strip()}\n"
    except Exception as e:
        full_text = f"\n\n--- {os.path.basename(file_path)} ---\n\nError: {e}\n"
    return full_text

def extract_from_folder(folder_path):
    """
    Extract text from all PDFs and images in a folder.
    """
    supported_ext = (".pdf", ".png", ".jpg", ".jpeg")
    all_text = ""

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(supported_ext):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing: {file_name} ...")
            all_text += extract_text_from_file(file_path)

    return all_text

if __name__ == "__main__":
    folder = r"C:\Users\ASUS\OneDrive\Desktop\Studies\python\file"  # Put all PDFs & images in this folder

    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' not found.")
    else:
        extracted_text = extract_from_folder(folder)

        # Print to console
        print("✅ Extracted Text:\n")
        print(extracted_text)

        # Save to output.txt
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print("\n💾 Extracted text saved to output.txt")
