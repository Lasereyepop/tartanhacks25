import requests
from dotenv import load_dotenv
import os
load_dotenv()
class supplement_engine:
    def __init__(self):
        self.init = True

    def query_web(self, topic):
        
            url = f"https://api.search.brave.com/res/v1/web/search?q={topic}"
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": os.getenv("BRAVE_API_KEY")
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()  # Parse the response as JSON
                # Extract titles and URLs
                results = data.get('web', {}).get('results', [])
                for result in results:
                    title = result.get('title')
                    url = result.get('url')
                    description = result.get('description')
                    age = result.get('page_age')
                    print(f"Title: {title}\nURL: {url}\n Description:{description}\n Age:{age}\n")
                    return (f"Title: {title}\nURL: {url}\n Description:{description}\n Age:{age}\n")
            else:
                print("Error TOPIC: ", topic)
                print(f"Error: {response.status_code}")

    def query_web_test(self):
        url = "https://api.search.brave.com/res/v1/web/search?q=hello+world!"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": os.getenv("BRAVE_API_KEY")
        }

        response = requests.get(url, headers=headers)
       

        if response.status_code == 200:
            data = response.json()  # Parse the response as JSON
            # Extract titles and URLs
            results = data.get('web', {}).get('results', [])
            for result in results:
                title = result.get('title')
                url = result.get('url')
                description = result.get('description')
                age = result.get('page_age')
                print(f"Title: {title}\nURL: {url}\n Description:{description}\n Age:{age}\n")
        else:
            print(f"Error: {response.status_code}")





