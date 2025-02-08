from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List
import json
import io
from topic_extract import topic_extractor  # Assuming you have the topic_extractor class from your code
from pdf_extraction import pdf_extractor  # Import your custom PDF extraction class

app = FastAPI()

class LinksResponse(BaseModel):
    topic: str
    links: List[str]

@app.post("/upload-pdf", response_model=List[LinksResponse])
async def upload_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    
    # Use your existing pdf_extract class to extract text from the PDF
    extractor = pdf_extractor(io.BytesIO(file_bytes))  # Instantiate your PDF extraction class
    print(file.filename)
    pdf_text = extractor.extract_pdf()  # Assuming extract_pdf is an async method
    print(pdf_text)

    processed_pdf = pdf_text.split("\n")
    # Process the extracted text (pass it to your topic_extractor or do any processing)
    extractor = topic_extractor(processed_pdf)
    extracted_topics = extractor.query()  # Assuming query() uses the extracted PDF text for processing
    
    if not extracted_topics:
        return []
    
    
    response = [
        LinksResponse(
            topic=topic,
            links=[
                f"https://example.com/{topic.replace(' ', '-')}",
                f"https://example.com/resources/{topic.replace(' ', '-')}",
                f"https://example.com/{topic.replace(' ', '-')}-guide"
            ]
        )
        for topic in extracted_topics if isinstance(topic, str)  # Ensure topic is a valid string
    ]

    
    return response
    # Convert extracted topics to a list if necessary
    # topics = json.loads(extracted_topics)

    # # Generate links for each topic
    # response = []
    # for topic in topics:
    #     links = [f"https://example.com/{topic.replace(' ', '-')}", 
    #              f"https://example.com/resources/{topic.replace(' ', '-')}", 
    #              f"https://example.com/{topic.replace(' ', '-')}-guide"]
    #     response.append(LinksResponse(topic=topic, links=links))

    # return response
