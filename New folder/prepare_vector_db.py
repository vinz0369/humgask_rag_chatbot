from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings

import os

# Cấu hình API Key
os.environ["MISTRAL_API_KEY"] = ""

pdf_data_path = "data"
vector_db_path = "vectorstores/db_faiss"

# tạo vector DB từ file
def create_db_from_files():
    loader = DirectoryLoader(pdf_data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    embedding_model = MistralAIEmbeddings(model="mistral-embed", default_batch_size=8)  # Chọn batch size phù hợp

    # Đưa vào FAISS Vector DB
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(vector_db_path)
    return db

create_db_from_files()
