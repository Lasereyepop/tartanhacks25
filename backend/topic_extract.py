from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

# MODEL_NAME = "deepseek/deepseek-r1-distill-llama-70b:free"
MODEL_NAME= "google/gemma-2-9b-it:free"
class topic_extractor:
    def __init__(self, text):
        self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key= os.getenv("DEEPSEEK_API_KEY"),
            )
        self.model = MODEL_NAME
        self.text = text

    def query(self):
        print(self.text)
        prompt = f"you are a highly intelligent bot capable of extracting keywords from convoluted files. More specifically, it will be extracted text from a syllabus. You will respond ONLY with an array of strings of key class topics you discover. DO NOT respond with any other dialouge. ONLY respond with an correctly formatted array of key topics seperated by commas ONLY: {self.text}" 
        completion = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            max_tokens=3000,
            model= self.model,
            messages=[
                {
                "role": "user",
                "content": prompt,
                }
            ]
        )
        try:
            print("complete")
            result=  completion.choices[0].message.content

            print(result)

            lines = result.strip().split(",")
                
                # Step 2: Clean up the lines (e.g., remove extra spaces, check for non-empty strings)
            topics = [line.strip() for line in lines if line.strip()]

                # Step 3: Ensure the result is a list of strings (topics)
            if isinstance(topics, list) and all(isinstance(topic, str) for topic in topics):
                return topics
            else:
                return []
                
                # Handle different possible issues with the string format
                # If it's a string that looks like a JSON array but has extra quotes or issues:
            

            #topics = json.loads(result)
           #if isinstance(topics, list):
        except Exception as e:
    # Catch general errors and print detailed information
            print("An error occurred:", str(e))
    
        

# topic_extractor = topic_extractor()

# print(topic_extractor.query())