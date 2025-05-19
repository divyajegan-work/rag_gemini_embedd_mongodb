from flask import Flask, request, render_template_string
import time
import numpy as np
from pymongo import MongoClient
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
client = MongoClient(os.getenv("MONGODB_URI"))
db = client['text_embeddings_db']
collection = db['embeddings']

def generate_embeddings(text):
    result = genai_client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text,
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
    )
    return result.embeddings[0].values

def store_embeddings(chunk, embedding):
    document = {
        "chunk": chunk,
        "embedding": embedding
    }
    collection.insert_one(document)

def split_text_into_chunks(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def process_text_and_store_embeddings(text):
    collection.delete_many({}) 
    chunks = split_text_into_chunks(text)
    for chunk in chunks:
        try:
            embedding = generate_embeddings(chunk)
            store_embeddings(chunk, embedding)
            print(f"Stored chunk: {chunk[:30]}...")
            time.sleep(1)
        except Exception as e:
            print(f"Failed to process chunk: {chunk[:30]}... Error: {e}")

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))            # dot product and linear algebra

def get_top_k_relevant_chunks(query, k=3):
    query_embedding = generate_embeddings(query)
    all_docs = list(collection.find({}))
    scored = []
    for doc in all_docs:
        similarity = cosine_similarity(query_embedding, doc['embedding'])
        scored.append((similarity, doc['chunk']))
    scored.sort(reverse=True, key=lambda x: x[0])   #want high score first
    return [chunk for _, chunk in scored[:k]]           #return k relevany onlyyy

def generate_structured_answer(query, context_chunks):
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction="You are an AI assistant providing structured answers.",
                context=context_chunks
            )
        )
        return response.text
    except Exception as e:
        print(f"Error generating structured answer: {e}")
        return None

global_warming_paragraph = """
Global warming refers to the long-term rise in Earth's average surface temperature due to human activities, primarily fossil fuel burning, which increases heat-trapping greenhouse gas levels in Earth's atmosphere. The consequences of global warming are vast and affect every region of the world. Melting glaciers and rising sea levels threaten coastal communities, while extreme weather patterns like droughts, floods, and hurricanes are becoming more frequent and intense. This warming disrupts ecosystems, endangers species, and affects agricultural productivity. Governments and organizations globally are pushing for policies to reduce carbon emissions, promote renewable energy, and protect forests. Public awareness and lifestyle changes are essential components of the fight against climate change. Renewable energy technologies, such as solar, wind, and hydro power, are gaining traction as sustainable alternatives. Reducing meat consumption, improving energy efficiency, and supporting green initiatives are some of the personal steps individuals can take. While climate change is a daunting challenge, it also presents an opportunity for innovation and global cooperation. Science continues to monitor and predict its impacts, providing critical data to guide policy and action. Immediate and sustained effort is required to mitigate the worst effects and secure a healthier planet for future generations.
"""  

process_text_and_store_embeddings(global_warming_paragraph)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Global Warming QA</title>
</head>
<body>
    <h1>Ask a Question About Global Warming</h1>
    <form method="POST">
        <input type="text" name="query" style="width: 400px;" required>
        <button type="submit">Submit</button>
    </form>

    {% if answer %}
        <h2>Structured Answer:</h2>
        <p>{{ answer }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        query = request.form["query"]
        context_chunks = get_top_k_relevant_chunks(query)
        answer = generate_structured_answer(query, context_chunks)
    return render_template_string(HTML_TEMPLATE, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)

"""
AIzaSyB3QAHVVdgmqWNT0gRceCWhlMfu7xI3AAY
"""