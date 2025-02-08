import pymupdf
import json

doc = pymupdf.open("1571_Syllabus.pdf")

# extract text 
pages = []

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text("text").encode("utf-8")

    if isinstance(text, bytes):
        text = text.decode("utf-8", errors="ignore")
    pages.append({"page":page_num+1, "text":text})



with open("output.json","w", encoding="utf-8") as json_file:
    json.dump(pages, json_file, indent=4, ensure_ascii=False)