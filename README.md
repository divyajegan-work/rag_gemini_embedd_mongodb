# mini-projects-python


## ⚙️ Setup Instructions

### 1. 🔐 Create a `.env` File

```env
GOOGLE_API_KEY=your_google_api_key_here
MONGODB_URI=your_mongodb_connection_string_here


# 🔍 RAG with Google Gemini + MongoDB

This project demonstrates a simple **Retrieval-Augmented Generation (RAG)** pipeline using **Google Gemini embeddings**, **MongoDB** for storage, and a **Flask web interface** for querying.

Users can ask questions about a given text (e.g., global warming), and the app returns structured answers by:
- Splitting and embedding the document,
- Storing embeddings in MongoDB,
- Retrieving top-matching chunks using semantic similarity,
- Passing them to Gemini for structured response generation.

---

## 🚀 Features

- 🔹 Embeds input text using **Gemini Embedding Model**
- 🔹 Stores text chunks and their embeddings in **MongoDB Atlas**
- 🔹 Uses **cosine similarity** to find top-k relevant passages
- 🔹 Generates structured responses using **Gemini 2.0 Flash**
- 🔹 Built with **Flask** and served via a simple web interface

---

## 🏗️ Project Structure
