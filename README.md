# ocr -> 
index.html + app.py -> are used to covert the pdf and image into the text file (.txt file) 

For proper working of this we has to install 3 things:
  1. pip install flask flask-cors pillow pytesseract pdf2image  (run in VS code terminal)
  2. Tesseract OCR (for image/text extraction)
    -> Download Link: https://github.com/UB-Mannheim/tesseract/wiki and then Set the path in Python code.
  3. Poppler (for PDF → image conversion)
     -> Download Link: https://github.com/oschwartz10612/poppler-windows/releases/ and then Set the  path in Python code.

Once you have completed this then open the terminal in vs code then run "python app.py"
Then open the HTML page and upload the file after that conversion of that file into the text file is download automatically.

ocr_multi -> is used for vs code  and it shows the output inside the vs code terminal 

ocr_api-> is used in the vs code and when we run it then it give the url link which is paste into the postman -> Collection then -> Post section in which the url is paste and they give the json in the form of output 
