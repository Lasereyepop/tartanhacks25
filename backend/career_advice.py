from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import os

class SyllabusAnalyzer:
    def __init__(self, user_syllabus, top_university_syllabi):
        
        load_dotenv()
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("DEEPSEEK_API_KEY"))
        self.user_syllabus = user_syllabus
        self.top_university_syllabi = top_university_syllabi

    def preprocess_topics(self, topics):
        return [topic.lower().strip() for topic in topics]

    def get_embeddings(self, topics):
        return self.embedding_model.encode(topics).tolist()

    def compare_topics(self, user_topics, university_topics, threshold=0.8):
        user_embeddings = self.get_embeddings(user_topics)
        university_embeddings = self.get_embeddings(university_topics)
        missing_topics = []
        
        for i, uni_topic in enumerate(university_topics):
            max_similarity = max(
                cosine_similarity([university_embeddings[i]], [user_embeddings[j]])[0][0]
                for j in range(len(user_topics))
            )
            if max_similarity < threshold:
                missing_topics.append(uni_topic)
        
        return missing_topics

    def compare_syllabi(self, threshold=0.8):
        missing_topics = {}
        user_topics = self.preprocess_topics(self.user_syllabus["topics"])
        
        for university, syllabus in self.top_university_syllabi.items():
            university_topics = self.preprocess_topics(syllabus["topics"])
            missing = self.compare_topics(user_topics, university_topics, threshold)
            if missing:
                missing_topics[university] = missing
        
        return missing_topics

    def generate_advice(self, missing_topics, career):
        model_name = "anthropic/claude-3.5-haiku"
        prompt = f"""
        I am a student studying algorithms. My syllabus covers: {', '.join(self.user_syllabus['topics'])}.
        However, I am missing the following topics compared to top university syllabi: {', '.join(missing_topics)}.
        I want to pursue a career as a {career}. Please provide specific advice on these aspects:
        
        1. How should I prioritize these missing topics?
        2. How can I integrate theoretical knowledge with practical exercises?
        3. What are the best resources (books, courses, websites) to learn these topics?
        4. Can you suggest projects that align with my career goals?
        5. What additional skills should I develop to complement my studies?
        7. What are industry trends related to these topics?
        
        Please provide concise and actionable advice.
        """
        
        completion = self.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a career and academic advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        return completion.choices[0].message.content

    def analyze(self, career):
        missing_topics = self.compare_syllabi()
        
        
       
        all_missing_topics = [topic for topics in missing_topics.values() for topic in topics]
        advice = self.generate_advice(all_missing_topics, career)
     
        return advice






