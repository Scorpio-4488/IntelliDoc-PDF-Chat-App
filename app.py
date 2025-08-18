import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.documents import Document

def get_pdf_text_and_metadata(pdf_docs):
    """Extracts text and metadata from a list of uploaded PDF files."""
    documents = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:
                documents.append(Document(
                    page_content=text,
                    metadata={'source': pdf.name, 'page': page_num + 1}
                ))
    return documents


def get_text_chunks(documents):
    """Splits a list of documents into smaller chunks for processing."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def get_vectorstore(text_chunks):
    """Generates a FAISS vector store from text chunks using Google embeddings."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(documents=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_rag_chain(vectorstore):
    """Creates a conversational retrieval chain with memory and question rewriting."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, convert_system_message_to_human=True)
    retriever = vectorstore.as_retriever()

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        ("human", "{chat_history}\n\nFollow Up Input: {input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

    qa_system_prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, just say that you don't know. Be concise and helpful."
        "\n\n{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        ("human", "{input}"),
    ])
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain


def main():
    """Main function to run the Streamlit application."""
    load_dotenv()
    st.set_page_config(page_title="IntelliDoc", page_icon="🧠")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            SystemMessage(content="Hello! I'm IntelliDoc. Upload your documents to get started.")
        ]

    with st.sidebar:
        st.title("🧠 IntelliDoc")
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs and click 'Process'", accept_multiple_files=True)
        
        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing documents..."):
                    documents = get_pdf_text_and_metadata(pdf_docs)
                    text_chunks = get_text_chunks(documents)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversation_rag_chain(vectorstore)
                    st.success("Processing complete!", icon="✅")
            else:
                st.warning("Please upload at least one PDF file.", icon="⚠️")

        if st.button("Clear Chat History"):
            st.session_state.chat_history = [
                SystemMessage(content="Hello! I'm IntelliDoc. Upload your documents to get started.")
            ]
            st.rerun()

        with st.expander("How to use IntelliDoc 🤔"):
            st.markdown("""
                1. **Upload your PDFs** using the uploader.
                2. Click the **Process** button.
                3. **Ask questions** about your documents in the chat box!
                4. View **source citations** for each answer.
                5. Click **Clear Chat History** to start a new conversation.
            """)

    st.header("Chat with your documents")
    
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if isinstance(message, SystemMessage):
                    with st.chat_message("assistant"):
                        st.markdown(message.content)
                elif message[0] == 'human':
                    with st.chat_message("user"):
                        st.markdown(message[1])
                elif message[0] == 'ai':
                    with st.chat_message("assistant"):
                        st.markdown(message[1])
                        if len(message) > 2 and message[2]:
                            st.markdown("---")
                            st.markdown("**Sources:**")
                            sources = set(f"{doc.metadata['source']} (Page {doc.metadata['page']})" for doc in message[2])
                            for source in sources.copy():
                                st.markdown(f"- {source}")

    user_question = st.chat_input("Ask a question about your documents...")
    if user_question:
        if st.session_state.conversation:
            with st.chat_message("user"):
                st.markdown(user_question)
            
            with st.chat_message("assistant"):
                stream = st.session_state.conversation.stream({
                    "chat_history": st.session_state.chat_history,
                    "input": user_question
                })
                response = st.write_stream(chunk["answer"] for chunk in stream if "answer" in chunk)

            st.session_state.chat_history.append(("human", user_question))
            st.session_state.chat_history.append(("ai", response, []))
            st.rerun()
        else:
            st.warning("Please upload and process your documents first.", icon="⚠️")


if __name__ == '__main__':
    main()