import json
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
            t_r = []
            if response.status_code == 200:
                data = response.json()  # Parse the response as JSON
                # Extract titles and URLs
                results = data.get('web', {}).get('results', [])
               
                for result in results:

                 
                    url = result

                    # title = result.get('title')
                    # url = result.get('url')
                    # description = result.get('description')
                    # age = result.get('page_age')
                    # print(f"Title: {title}\nURL: {url}\n Description:{description}\n Age:{age}\n")
                    t_r.append(f"URL: {url}\n ")
                    
            else:
                print("Error TOPIC: ", topic)
                print(f"Error: {response.status_code}")
            
            return t_r

    def query_video(self, topic):
        url = f"https://api.search.brave.com/res/v1/videos/search?q={topic}&freshness=py"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": os.getenv("BRAVE_API_KEY")
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
         

            results = data.get('results', [])
            results_tr = []
            for result in results:
                title = result.get('title')
                url = result.get('url')
                description = result.get('description')
                video = result.get('video')
                views = video.get('views')
                thumbnail = result.get('thumbnail')
                results_tr.append({
                    "title": title, 
                    "url": url,
                    "description": description,
                    "views": 0 if views==None else views,
                    "thumbnail": "" if thumbnail==None else thumbnail.get('src'),
                })
                
               # print(f"Title: {title}\nURL:{url}\ndescription{description}\nviews:{views}")
            sorted_results = sorted(results_tr, key=lambda x: x["views"], reverse=True)
            return sorted_results
            top_views = top_views = [f'"url": {item.get("url","")}, "title": {item.get("title", "")}, "thumbnail": {item.get("thumbnail", "")}' for item in sorted_results][:5]
         

            
        else:
            return []


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





