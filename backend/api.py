from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
import json
import io
from topic_extract import topic_extractor  # Assuming you have the topic_extractor class from your code
from pdf_extraction import pdf_extractor  # Import your custom PDF extraction class
from supplement_engine import *
from ranking_engine import ranking_engine

MODEL_NAME="google/gemma-2-9b-it:free"
app = FastAPI()

class VideoLink(BaseModel):
    title: str
    url: str
    description: str
    views: int
    thumbnail: str

class LinksResponse(BaseModel):
    topic: str
    links: List[str]
    video_links: Optional[List[VideoLink]] = None

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
    
    s_l = supplement_engine()
    r_l = ranking_engine(MODEL_NAME)

    
    # response = [
    #     LinksResponse(
    #         topic=topic,
    #         links=get_links(topic, s_l, r_l),
    #         video_links=[
    #         VideoLink(
    #             title=video['title'],
    #             url=video['url'],
    #             thumbnail=video['thumbnail']
    #         )
    #         for video in s_l.query_video(topic)
    #         ]
    #     )
    #     for topic in extracted_topics[:10] if isinstance(topic, str)  # Ensure topic is a valid string
    # ]

    response = []

    for topic in extracted_topics[:10]:
        if isinstance(topic,str):
            video_responses = s_l.query_video(topic)
            video_links = [
                VideoLink(
                    title=video['title'],
                    description=video['description'],
                    views=video['views'],
                    url=video['url'],
                    thumbnail=video['thumbnail']
                )
            for video in video_responses
        ]
            response.append(
            LinksResponse(
                topic=topic,
                links=get_links(topic, s_l, r_l),
                video_links=video_links

            )
            )

    
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


def get_links(topic, supplement_engine, ranking_engine):
    print("got here")
    s_l = supplement_engine
    r_l = ranking_engine

    web_results = s_l.query_web(topic)
    ranked_links = r_l.return_links(web_results)

    return ranked_links

    
