from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

MODEL_NAME = "deepseek/deepseek-r1-distill-llama-70b:free"
class topic_extractor:
    def __init__(self):
        self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key= os.getenv("DEEPSEEK_API_KEY"),
            )
        self.model = MODEL_NAME

    def query(self) -> str:
        with open("syllabus_schedule.json", "r") as file:

            data = json.load(file)
        
        json_string = json.dumps(data)
        prompt = f"you are a highly intelligent bot capable of extracting keywords from convoluted files. More specifically, it will be extracted text from a syllabus. You will respond ONLY with an array of strings of key class topics you discover. DO NOT respond with any other dialouge. ONLY respond with an array of key topics: {json_string}" 
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
                "content": prompt,\
                }
            ]
        )
        try:
            print("complete")
            return completion.choices[0].message.content
        except:
            print(f"Error generating output: {completion.error['metadata']['raw']}")
            return None
        

topic_extractor = topic_extractor()

print(topic_extractor.query())