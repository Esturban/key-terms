
from docx import Document
from PyPDF2 import PdfFileReader
import os
from .ttk import extract_keywords
import logging

import json
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()
        return text
    
def process_files(data_folder, output_folder,logger):
    results = {}
    
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        
        if filename.endswith('.docx'):
            logger.info(f'Processing file: {filename}')
            text = extract_text_from_docx(file_path)
        elif filename.endswith('.pdf'):
            logger.info(f'Processing file: {filename}')
            text = extract_text_from_pdf(file_path)
        else:
            continue

        keywords = extract_keywords(text)
        results[filename] = keywords
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, 'results.json')
    with open(output_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)