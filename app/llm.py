import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_and_split_docs():
    loader = PyPDFLoader("knowledge_base/customer_guidelines.pdf")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(documents)

def create_vectorstore():
    documents = load_and_split_docs()
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

vectorstore = create_vectorstore()

def rag_response(query):
    retriever = vectorstore.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0),
        retriever=retriever
    )
    return qa.run(query)
