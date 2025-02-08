from openai import OpenAI
import os
import json
from dotenv import load_dotenv

MODEL_NAME="anthropic/claude-3.5-haiku"
load_dotenv()
better_universities = ["MIT", "Standford", "CMU", "UC Berkeley", "Harvard", "Cornell", "Princeton"]
prompt = "You are a search machine with two outputs, None or a JSON file. No matter what, you may only output either None or a JSON file. Given a json payloud of a user's university , course number, course name, and target universites, find two similar courses from those universities. Format your output as a JSON file like so: { \"course\": course_name, \"link\": link_to_course, \"university\": university, \"course_2\": course_2_name, \"link_2\": link_to_course_2, \"university_2\": university_2} Follow this output EXACTLY. IF you cannot find it, return NULL" 

class search_syllabus:
    def __init__(self, model_name):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        self.model_name = model_name

    def search_for_syllabus(self, user_university, user_course_number, user_course_name, user_target_uni):
        payload = {
            "user_university": user_university,
            "user_course_number": user_course_number,
            "user_course_name": user_course_name,
            "user_target_uni": user_target_uni
        }
        payload_string = json.dumps(payload)

        p = prompt + "payload: " + payload_string

        
        completion = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<>",
                "X-Title": "<>",
            },
            max_tokens = 500,
            model = self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": p,
                }
            ]
        )
        try:
            result=completion.choices[0].message.content

            
            
            return json.loads(result)
            

        except:
            print("error")

        