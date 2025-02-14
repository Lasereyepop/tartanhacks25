from time import sleep
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import io
from topic_extract import topic_extractor  # Assuming you have the topic_extractor class from your code
from pdf_extraction import pdf_extractor  # Import your custom PDF extraction class
from supplement_engine import *
from ranking_engine import ranking_engine
from test_web_scraping import web_scraper
from search_syllabus import search_syllabus
from career_advice import SyllabusAnalyzer

MODEL_NAME="openai/gpt-4o-mini"
SYLLABUS_NAME="anthropic/claude-3.5-haiku"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


class SyllabusResponse(BaseModel):
    course: str
    link: str
    university: str
    course_2: str
    link_2: str
    university_2: str

class ClassComparisonResponse(BaseModel):
    topic_1: str
    topic_2: str
    topic_3: str

class CareerAdviceResponse(BaseModel):
    response: str

@app.post("/career-advice", response_model=CareerAdviceResponse)
async def career_advice(user_syllabus, top_syllabi, career):
    c_r = SyllabusAnalyzer(json.loads(user_syllabus), json.loads(top_syllabi))
    result = c_r.analyze(career)
    if result is None:
        return CareerAdviceResponse(
            response=""
        )
    else:
        return CareerAdviceResponse(
            response=result
        )


@app.post("/compare-classes", response_model=ClassComparisonResponse)
async def compare_classes(class_1, class_2, class_1_university, class_2_university):
    s_s = search_syllabus(SYLLABUS_NAME)
    t_r = s_s.compare_classes(class_1, class_2, class_1_university, class_2_university)
    if t_r is None:
        return ClassComparisonResponse(
            topic_1="",
            topic_2="",
            topic_3=""
        )
    else:
        return ClassComparisonResponse(
            topic_1=t_r['topic_1'],
            topic_2=t_r['topic_2'],
            topic_3=t_r['topic_3']
        )

@app.post("/upload-course-information", response_model=SyllabusResponse)
async def upload_course_information(user_university, user_course_number, user_course_name, user_target_uni):
    s_s = search_syllabus(SYLLABUS_NAME)
    t_r = s_s.search_for_syllabus(user_university, user_course_number, user_course_name, user_target_uni)
    if t_r is None:
        return SyllabusResponse(
            course="",
            link="",
            university=""
        )
    else:
        return SyllabusResponse(
            course=t_r['course'],
            link=t_r['link'],
            university=t_r['university'],
            course_2=t_r['course_2'],
            link_2=t_r['link_2'],
            university_2=t_r['university_2']
        )

@app.post("/upload-url", response_model=List[LinksResponse])
async def upload_url(url: str):
    w_s = web_scraper(url)

    result = w_s.scrape_syllabus()

    extractor = topic_extractor(result)
    extracted_topics = extractor.query()  # Assuming query() uses the extracted PDF text for processing

    if not extracted_topics:
        return []
    
    s_l = supplement_engine()
    r_l = ranking_engine(MODEL_NAME)

    response = []

    for topic in extracted_topics[:10]:
        if isinstance(topic, str):
            links =get_links(topic, s_l, r_l)
            sleep(2)
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
                    links=links,
                    video_links=video_links
                )
            )
    
    return response


    


@app.post("/upload-pdf", response_model=List[LinksResponse])
async def upload_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    
    # Use your existing pdf_extract class to extract text from the PDF
    extractor = pdf_extractor(io.BytesIO(file_bytes))  # Instantiate your PDF extraction class
   
    pdf_text = extractor.extract_pdf()  # Assuming extract_pdf is an async method

    processed_pdf = pdf_text.split("\n")
    # Process the extracted text (pass it to your topic_extractor or do any processing)
    extractor = topic_extractor(processed_pdf)
    extracted_topics = extractor.query()  # Assuming query() uses the extracted PDF text for processing
    
    if not extracted_topics:
        return []
    
    s_l = supplement_engine()
    r_l = ranking_engine(MODEL_NAME)

    response = []

    for topic in extracted_topics[:10]:
        if isinstance(topic, str):
            links =get_links(topic, s_l, r_l)
            sleep(2)
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
                    links=links,
                    video_links=video_links
                )
            )
    
    return response

def get_links(topic, supplement_engine, ranking_engine):
   
    s_l = supplement_engine
    r_l = ranking_engine
    sleep(1)
    web_results = s_l.query_web(topic)
    sleep(1)
    ranked_links = r_l.return_links(web_results)
    

    return ranked_links
