import nltk
import nltk.data
nltk.data.path.append('./data')
nltk.download('punkt_tab', download_dir='data')
nltk.download('stopwords', download_dir='data')
import os
import json
import logging
from docx import Document
from PyPDF2 import PdfFileReader
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def extract_keywords(text, n=10):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    word_freq = Counter(words)
    return word_freq.most_common(n)

def process_files(data_folder, output_folder):
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

if __name__ == "__main__":
    data_folder = 'data'
    output_folder = 'output'
    process_files(data_folder, output_folder)