import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Cấu hình API Key từ biến môi trường
os.environ["MISTRAL_API_KEY"] = "gV0ZrsZjs5RKuaReOWn1zCtjjTCNIPd9"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Định nghĩa đường dẫn
PDF_DATA_PATH = "data"
VECTOR_DB_PATH = "vectorstores/db_faiss"

# Hàm tạo hoặc cập nhật FAISS
def create_or_update_db():
    print("[INFO] Đang load tài liệu PDF...")
    loader = DirectoryLoader(PDF_DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    print("[INFO] Chia nhỏ văn bản...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    print("[INFO] Tạo vector embedding...")
    embedding_model = MistralAIEmbeddings(model="mistral-embed")

    if os.path.exists(VECTOR_DB_PATH):
        print("[INFO] Tải FAISS hiện có và cập nhật dữ liệu mới...")
        db = FAISS.load_local(VECTOR_DB_PATH, embedding_model, allow_dangerous_deserialization=True)
        db.add_documents(chunks)  # Thêm dữ liệu mới
    else:
        print("[INFO] Tạo FAISS mới...")
        db = FAISS.from_documents(chunks, embedding_model)

    db.save_local(VECTOR_DB_PATH)
    print("[SUCCESS] VectorDB đã được cập nhật thành công!")
    return db

# Load VectorDB
def load_vector_db():
    print("[INFO] Đang load VectorDB...")
    embedding_model = MistralAIEmbeddings(model="mistral-embed")
    db = FAISS.load_local(VECTOR_DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

# Load Mistral LLM
def load_llm():
    print("[INFO] Đang khởi tạo Mistral LLM...")
    llm = ChatMistralAI(
    model="mistral-large-latest",
    api_key=MISTRAL_API_KEY,
    temperature=0.7,  # Tăng nhiệt độ để câu trả lời phong phú hơn
    max_tokens=1024   # Tăng số lượng token đầu ra
)

    return llm

# Tạo Prompt Template
def create_prompt():
    template = """<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu không có thông tin, hãy trả lời "Tôi không biết".\n{context}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant"""
    return PromptTemplate(template=template, input_variables=["context", "question"])

# Xử lý lỗi quá tải API (429)
def retry_with_backoff(func, retries=3, delay=10):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e):
                print(f"[WARNING] Lỗi rate limit (429), thử lại sau {delay} giây...")
                time.sleep(delay)
            else:
                raise e
    raise Exception("[ERROR] Quá số lần thử, dừng lại.")

# Tạo Chain RAG
def create_qa_chain():
    db = load_vector_db()
    llm = retry_with_backoff(load_llm)
    prompt = create_prompt()

    print("[INFO] Tạo pipeline RAG...")
    qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 8}),  # Tăng số đoạn truy xuất
    return_source_documents=False,
    chain_type_kwargs={'prompt': prompt}
)

    return qa_chain

# Trả lời câu hỏi
def answer_question(question):
    qa_chain = create_qa_chain()
    question = question.lower().strip()  # Chuẩn hóa câu hỏi
    response = qa_chain.invoke({"query": question})
    return response

# Chạy thử nghiệm
if __name__ == "__main__":
    if not os.path.exists(VECTOR_DB_PATH):
        create_or_update_db()

    question = "Đại học Mỏ thành lập năm nào?"
    response = answer_question(question)
    print("[ANSWER]", response)
