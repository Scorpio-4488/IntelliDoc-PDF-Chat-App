# 🧠 IntelliDoc: Advanced PDF Chat Application

![IntelliDoc App Demo](https://github.com/Scorpio-4488/IntelliDoc-PDF-Chat-App/blob/main/intellidoc-demo.gif?raw=true)
*A live, interactive demo is available here: [**IntelliDoc Live App**](https://intellidoc-pdf-chat-app.streamlit.app/)*

---

This is an advanced RAG (Retrieval-Augmented Generation) application built with LangChain and Streamlit that allows you to have intelligent conversations with your PDF documents. The app is designed to be a robust, user-friendly tool for extracting and interacting with information locked in your files.

## ✨ Key Features

- **Interactive & Polished UI:** A sleek, user-friendly interface built with a custom Streamlit theme for a professional look and feel.
- **Multi-PDF Support:** Upload and chat with multiple PDF documents simultaneously.
- **Source Citations:** Every answer is backed by citations, referencing the specific source document and page number to ensure trustworthiness.
- **Advanced Conversational Memory:** The AI remembers the context of the conversation and intelligently rephrases follow-up questions for accurate document retrieval.
- **Real-time Streaming Responses:** Answers are streamed token-by-token, providing an immediate and responsive user experience similar to leading AI chatbots.

## 🛠️ Tech Stack

- **Backend:** Python
- **AI Framework:** LangChain
- **LLM & Embeddings:** Google Gemini & Google AI Platform
- **Vector Store:** FAISS (Facebook AI Similarity Search)
- **UI & Deployment:** Streamlit & Streamlit Community Cloud
- **PDF Processing:** PyPDF2

## 🚀 How to Run Locally

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.9+
- A Google API Key with the Gemini API enabled.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/Scorpio-4488/IntelliDoc-PDF-Chat-App.git](https://github.com/Scorpio-4488/IntelliDoc-PDF-Chat-App.git)
    cd IntelliDoc-PDF-Chat-App
    ```
2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Set up your environment variables:**
    - Create a file named `.env` in the root of the project.
    - Add your Google API key to the file:
      ```
      GOOGLE_API_KEY="AIzaSyYourApiKeyHere"
      ```
5.  **Run the Streamlit application:**
    ```sh
    streamlit run app.py
    ```

## 📜 License

This project is licensed under the MIT License.

## 👤 Author

- **Sagar Sahu**
- **GitHub:** `https://github.com/Scorpio-4488`
- **LinkedIn:** `www.linkedin.com/in/sagar-sahu-a888a5367`


