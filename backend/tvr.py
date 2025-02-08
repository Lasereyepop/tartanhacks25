import fitz  
from bertopic import BERTopic  
from keybert import KeyBERT  
import nltk  
from nltk.corpus import stopwords
import json

#nltk.download('stopwords') 
def extract_keywords(num_keywords=25):
    try:
        with open("output.json", "r") as file:

            data = json.load(file)
        
        json_string = json.dumps(data)

     
        kw_model = KeyBERT('distilbert-base-nli-mean-tokens')
        keywords = kw_model.extract_keywords(json_string, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=num_keywords)
        return [kw[0] for kw in keywords]  # return only keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

def extract_topics():
  

        with open("output.json", "r") as file:
            print(file)
            data = json.load(file)
        
        json_string = json.dumps(data)

        print(json_string)
        
        topic_model = BERTopic(language="english")
        topics, _ = topic_model.fit_transform([json_string])
        return topic_model.get_topic_info()
        
keywords = extract_keywords()

print(keywords)