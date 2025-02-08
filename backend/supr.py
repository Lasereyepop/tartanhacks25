import json
import openai
from googlesearch import search
from numpy import dot
from numpy.linalg import norm
import logging
import os
from dotenv import load_dotenv

load_dotenv()
# Set your OpenAI API key
OPENAI_API_KEY = "your-api-key"
openai.api_key = os.getenv("OPEN_AI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_top_url(query):
    try:
        results = search(query, num=1, stop=1)
        return next(results)
    except Exception as e:
        logging.error(f"Error fetching URL for query '{query}': {e}")
        return "URL not found"

def attach_dynamic_urls(resources):
    return [{"topic": res, "url": get_top_url(res)} for res in resources]

def rank_resources(resources):
    return sorted(resources, key=lambda x: len(x), reverse=True)

def trim_resources(resources, max_length=10):
    return resources[:max_length]

def validate_resources(resources):
    return [res for res in resources if len(res) > 5]

def search_with_openai(query, topics):
    response = openai.Embedding.create(
        input=[query] + topics,
        model="text-embedding-ada-002"
    )

    query_embedding = response["data"][0]["embedding"]
    topic_embeddings = [entry["embedding"] for entry in response["data"][1:]]

    # Calculate similarity scores (cosine similarity)
    scores = [dot(query_embedding, topic_embedding) / (norm(query_embedding) * norm(topic_embedding))
              for topic_embedding in topic_embeddings]

    # Rank topics based on similarity
    ranked_topics = sorted(zip(topics, scores), key=lambda x: x[1], reverse=True)
    return [topic for topic, score in ranked_topics[:10]]  # Return top 10 results

def main():
    try:
        # Load JSON data
        with open("topics.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading topics.json: {e}")
        return

    topics = data.get("topics", [])  # Extract topics

    # Perform search using OpenAI embeddings
    search_results = search_with_openai("Quantum Computation", topics)

    # Rank, trim, and validate results
    ranked_results = rank_resources(search_results)
    trimmed_results = trim_resources(ranked_results)
    valid_results = validate_resources(trimmed_results)

    # Attach URLs
    valid_results_with_urls = attach_dynamic_urls(valid_results)

    # Save results
    try:
        with open("validated_search_results.json", "w") as json_file:
            json.dump(valid_results_with_urls, json_file, indent=4)
        logging.info(f"Search results with URLs saved to validated_search_results.json")
    except Exception as e:
        logging.error(f"Error saving results to validated_search_results.json: {e}")

    # Print the validated results
    logging.info(f"Search results with URLs: {valid_results_with_urls}")

if __name__ == '__main__':
    main()
