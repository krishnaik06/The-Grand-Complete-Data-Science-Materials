from flask import Flask, render_template, request, redirect, url_for
from ocr_engine import OCREngine
from pdf_extractor import extract_text_from_pdf
from utils.helper import allowed_file, save_uploaded_file
from keyword_extract import extract_keywords
from yake import KeywordExtractor
import os
import spacy
import yake

# Load the English language model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=20)

#custom_kw_extractor = yake.KeywordExtractor(lan="hin+eng")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        file_type = request.form['file-type']

        if file and allowed_file(file.filename):
            filename = save_uploaded_file(file)
            if filename:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                extracted_text = ""

                if file_type == 'image':
                    ocr = OCREngine()
                    extracted_text = ocr.extract_text(file_path)
                elif file_type == 'pdf':
                    extracted_text = extract_text_from_pdf(file_path)

                # Extract keywords using YAKE
                keywords = kw_extractor.extract_keywords(extracted_text)
                #keywords = custom_kw_extractor.extract_keywords(extracted_text)

                # Extract the keyword text from YAKE results
                extracted_keywords = [keyword[0] for keyword in keywords]

                return render_template('index.html', extracted_text=extracted_text, extracted_keywords=extracted_keywords)

    # Show the home page for both GET and POST requests
    return render_template('index.html', extracted_text=None)

if __name__ == '__main__':
    app.run(debug=True)
