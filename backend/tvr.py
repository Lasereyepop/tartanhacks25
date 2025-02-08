import fitz  
import pdfplumber  
from bertopic import BERTopic  
from keybert import KeyBERT  
import nltk  
from nltk.corpus import stopwords

nltk.download('stopwords') 
def extract_keywords(text, num_keywords=5):
    try:
        kw_model = KeyBERT('distilbert-base-nli-mean-tokens')
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=num_keywords)
        return [kw[0] for kw in keywords]  # return only keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

def extract_topics(text):
    try:
        topic_model = BERTopic(language="english")
        topics, _ = topic_model.fit_transform([text])
        return topic_model.get_topic_info()
    except Exception as e:
        print(f"Error extracting topics: {e}")
        return None