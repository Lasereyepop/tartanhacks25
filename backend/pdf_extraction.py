import pymupdf
import json
import re

doc = pymupdf.open("1571_Syllabus.pdf")

# extract text 
pages = []
def preprocess_text(page):
    text = page["text"]
    text = re.sub(r"\s{2,}", "\n", text)
    text = re.sub(r"[\u2022•▪✔]", "- ", text)
    text = re.sub(r"[-–—]+\s*", "- ", text)  # Dashes as bullets
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # Remove non-ASCII characters
    text = re.sub(r"[“”]", "\"", text)  # Normalize quotes
    text = re.sub(r"[‘’]", "'", text)   # Normalize apostrophes
    text = re.sub(r"Page\s*\d+", "", text)  # Remove "Page 1" type footers
    text = re.sub(r"\b(Syllabus|Course Outline|Contents)\b", "", text, flags=re.IGNORECASE)  # Remove generic headers
    text = re.sub(r"(\w)\n(\w)", r"\1 \2", text)  # Join words split across lines
    
    return text.strip()
   


for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text("text").encode("utf-8")

    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="ignore")
    pages.append({"page":page_num+1, "text":text})


for page in pages:
    page["text"] = preprocess_text(page)


with open("output.json","w", encoding="utf-8") as json_file:
    json.dump(pages, json_file, indent=4, ensure_ascii=False)




