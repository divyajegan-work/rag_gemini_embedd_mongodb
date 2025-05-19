from flask import Flask, request, jsonify
import PyPDF2
import requests
import numpy as np
from pymongo import MongoClient
from langchain_text_splitters import CharacterTextSplitter
import google.generativeai as genai

app = Flask(__name__)

client = MongoClient("MONGODB_URI")
db = client['pdf_db']
collection = db['pdf_chunks']

genai.configure(api_key="GOOGLE_API_KEY")
EMBED_MODEL = "text-embedding-004"
GEN_MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return "".join([page.extract_text() or "" for page in reader.pages])


def get_embedding(text):
    response = genai.embed_content(model=EMBED_MODEL, content=text, task_type="retrieval_document")
    return response["embedding"]


def chunk_text(text):
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=200, chunk_overlap=20
    )
    return splitter.split_text(text)


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        text = extract_text_from_pdf(pdf_file)
        chunks = chunk_text(text)

        collection.delete_many({})
        for chunk in chunks:
            embedding = get_embedding(chunk)
            collection.insert_one({
                "text": chunk,
                "embedding": embedding
            })

        return jsonify({"message": "PDF uploaded and embedded chunks stored in MongoDB."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is missing"}), 400

    query_embedding = get_embedding(query)

    best_score = -1
    best_chunk = ""
    for doc in collection.find():
        doc_embedding = np.array(doc["embedding"])
        score = np.dot(query_embedding, doc_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
        if score > best_score:
            best_score = score
            best_chunk = doc["text"]

    prompt = {
        "contents": [{"parts": [{"text": f"{best_chunk}\n\nQuestion: {query}"}]}],
        "generationConfig": {"temperature": 0.7}
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(GEN_MODEL_URL + "?key=GEMINI_API_KEY", json=prompt, headers=headers)

    if response.status_code == 200:
        try:
            answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"answer": answer}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to parse response: {str(e)}"}), 500
    else:
        return jsonify({"error": "Gemini API failed"}), 500

@app.route('/')
def home():
    return " RAG with Gemini, MongoDB, and LangChain you can upload pdf"

if __name__ == '__main__':
    app.run(debug=True)
