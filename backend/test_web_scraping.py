import requests
import re
from bs4 import BeautifulSoup

def scrape_syllabus(url, keywords=None):
    if keywords is None:
        keywords = ["schedule","week","topic","lecture","session","date","calendar"]

        try:

            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            #regex pattern
            pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)

            matches = soup.find_all(string=pattern)

            schedule=[]

            for match in matches:
                parent = match.parent

                for elem in parent.find_all_next(['table','ul','ol','div']):
                    if elem.name == 'table':
                        rows = elem.find_all('tr')
                        for row in rows:
                            cols = [col.get_text(strip=True) for col in row.find_all(['td','th'])]
                            if cols:
                                schedule.append(cols)
                        break
                    elif elem.name in ['ul', 'ol']:
                        items = [li.get_text(strip=True) for li in elem.find_all('li')]

                        if items:
                            schedule.extend(items)
                        break
                    elif elem.name == 'div':

                        children = elem.find_all(['p','span','div'])
                        if children:
                            texts = [child.get_text(strip=True) for child in children if child.get_text(strip=True)]
                            schedule.extend(texts)
                            break
            return schedule


        except requests.RequestException as e:
            print(f"connection error: {e}")
            return None
        
url = "https://www.cs.cmu.edu/~112/schedule.html"

schedule = scrape_syllabus(url)
if schedule:
    for entry in schedule:
        print(entry)
