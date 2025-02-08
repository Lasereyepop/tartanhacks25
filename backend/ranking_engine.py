from openai import OpenAI
import os
from dotenv import load_dotenv
from urlextract import URLExtract
import re
prompt = """
You are a highly intelligent ratings bot. Given a list of web results, your task is to return the most relevant links Prioritize websites from academic sources, particularly those ending in ".edu". Choose sites that are most likely to help a college student learn the site's topic. Respond only with the list of RLs, separated by commas. Do not include any additional text, explanations, or apologies. If no relevant links are found, return nothing. IT IS ESSENTIAL YOU DO THIS
"""
class ranking_engine:
    def __init__(self, model_name):
            self.client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key= os.getenv("DEEPSEEK_API_KEY"),
                )
            self.model = model_name
    
    def return_links(self, input_data):
        # pseudo
        to_send = prompt + f"data: {input_data}"
        completion = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<>",
                "X-Title": "<>",
            },
            max_tokens = 500,
            model = self.model,
            messages=[
                {
                    "role": "user",
                    "content": to_send,
                }
            ]
        )
        try:
            result=completion.choices[0].message.content
            print("LIST RANK RESULT: ", result)
            lines = result.strip().split(",")

            returns= [line.strip() for line in lines if line.strip()]

            

            if isinstance(returns, list) and all(isinstance(r, str) for r in returns):
                 return returns
            
            else:
                return []
        except:
            print(f"Error generating output: ")
            return []

        # step 1: make a good ass prompt


        #step 2: query fingers crossed get list of links that i don't have to move mountains to format


        #step 3: return append to thing in api