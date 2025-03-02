
import nltk
import nltk.data
nltk.data.path.append('./data')
nltk.download('punkt_tab', download_dir='data')
nltk.download('stopwords', download_dir='data')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

def extract_keywords(text, n=10):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    word_freq = Counter(words)
    return word_freq.most_common(n)
