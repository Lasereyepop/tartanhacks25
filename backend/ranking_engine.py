from openai import OpenAI
import os
from dotenv import load_dotenv
prompt = """
you are a highly intelligent ratings bot that, given a list of web results, returns the 5 most relevant links. Choose based off how credible and educational the websites are. 
Favor websites from academic sources, such as ending with '.edu'. Pick sites that are most likely to help a college student learn the site's topic. Return as a list of strings seperated by commas. 
ONLY return this list. return NOTHING ELSE. 
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