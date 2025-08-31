import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import tempfile
import os

# Optional fallback for Streamlit async issues
import nest_asyncio
import asyncio
nest_asyncio.apply()

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    st.error("⚠️ GOOGLE_API_KEY not found in .env!")
else:
    os.environ["GOOGLE_API_KEY"] = google_api_key

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("📄 PDF Chatbot")
st.write("Ask questions about your PDF documents!")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    # Save uploaded file to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # ------------------------------
    # Load and split PDF
    # ------------------------------
    loader = PyPDFLoader(tmp_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    docs = text_splitter.split_documents(data)
    st.write(f"✅ PDF loaded and split into {len(docs)} chunks.")

    # ------------------------------
    # Embeddings & Vectorstore
    # ------------------------------
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # ------------------------------
    # LLM & RAG chain
    # ------------------------------
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, max_tokens=500)

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise.\n\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # ------------------------------
    # User Query
    # ------------------------------
    user_question = st.text_input("Ask a question about the PDF:")

    if user_question:
        try:
            # First try synchronous invocation
            response = rag_chain.invoke({"input": user_question})
        except RuntimeError:
            # Fallback: run explicitly in event loop
            loop = asyncio.get_event_loop()
            response = loop.run_until_complete(rag_chain.invoke({"input": user_question}))

        st.write("**Answer:**")
        st.success(response["answer"])
