import requests
import re
from bs4 import BeautifulSoup

def scrape_syllabus(url, keywords=None):
    # Set a default list of keywords if none are provided
    if keywords is None:
        keywords = ["schedule", "week", "topic", "lecture", "session", "date", "calendar", "agenda", "course", "plan", "module", "outline"]

    try:
        # Fetch webpage
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Case-insensitive regex pattern for keywords
        pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)

        # Find all elements containing keywords (headings, paragraphs, etc.)
        matches = soup.find_all(string=pattern)

        schedule = []

        for match in matches:
            # Navigate to the parent element (e.g., <h2>, <div>)
            parent = match.parent

            # Look for the closest relevant elements after the keyword
            for elem in parent.find_all_next(['table', 'ul', 'ol', 'div', 'p', 'section', 'article', 'span', 'header']):
                # Extract data based on element type
                if elem.name == 'table':
                    rows = elem.find_all('tr')
                    for row in rows:
                        cols = [col.get_text(strip=True) for col in row.find_all(['td', 'th'])]
                        if cols:
                            schedule.append(cols)
                    break  # Stop after the first valid table
                elif elem.name in ['ul', 'ol']:
                    items = [li.get_text(strip=True) for li in elem.find_all('li')]
                    if items:
                        schedule.extend(items)
                    break  # Stop after the first valid list
                elif elem.name == 'div':
                    # Check if the div has nested structure (e.g., dates/topics in spans)
                    children = elem.find_all(['p', 'span', 'div'])
                    if children:
                        texts = [child.get_text(strip=True) for child in children if child.get_text(strip=True)]
                        schedule.extend(texts)
                        break
                elif elem.name == 'p':
                    text = elem.get_text(strip=True)
                    if text:
                        schedule.append(text)
                        break
                elif elem.name == 'section':
                    # Check section for nested content
                    content = [child.get_text(strip=True) for child in elem.find_all(['p', 'span', 'div']) if child.get_text(strip=True)]
                    if content:
                        schedule.extend(content)
                    break
                elif elem.name == 'article':
                    # Check article for nested content
                    content = [child.get_text(strip=True) for child in elem.find_all(['p', 'span', 'div']) if child.get_text(strip=True)]
                    if content:
                        schedule.extend(content)
                    break
                elif elem.name == 'span':
                    # Check span for inline content
                    content = elem.get_text(strip=True)
                    if content:
                        schedule.append(content)
                    break
                elif elem.name == 'header':
                    # Check header for relevant text
                    content = [child.get_text(strip=True) for child in elem.find_all(['p', 'span', 'div']) if child.get_text(strip=True)]
                    if content:
                        schedule.extend(content)
                    break

        return schedule

    except requests.RequestException as e:
        print(f"Connection error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
url = "https://www.cs.princeton.edu/courses/archive/spring25/cos226/lectures.php"
schedule = scrape_syllabus(url)
if schedule:
    for entry in schedule:
        print(entry)
