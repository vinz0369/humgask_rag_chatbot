import os
import streamlit as st
from langchain.chains import RetrievalQA

from chat import create_db_from_files, create_qa_chain, VECTOR_DB_PATH

st.set_page_config(page_title="Chatbot hỏi đáp PDF", layout="wide")
st.title("📚 Chatbot hỏi đáp tài liệu PDF")

st.sidebar.header("📂 Quản lý tài liệu")
uploaded_files = st.sidebar.file_uploader("Tải lên file PDF", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    os.makedirs("data", exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join("data", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
    st.sidebar.success("📂 Tệp đã được tải lên thành công!")

if st.sidebar.button("🔄 Tạo Cơ sở Dữ liệu Vector"):
    with st.spinner("Đang xử lý tài liệu..."):
        create_db_from_files()
    st.sidebar.success("✅ VectorDB đã được tạo!")

# Kiểm tra xem VectorDB đã tồn tại chưa
if not os.path.exists(VECTOR_DB_PATH):
    st.warning("⚠️ Cơ sở dữ liệu vector chưa được tạo. Hãy tải lên tài liệu và nhấn 'Tạo Cơ sở Dữ liệu Vector'.")
else:
    # Khởi tạo chatbot
    qa_chain = create_qa_chain()
    
    # Giao diện chat
    st.subheader("💬 Chatbot hỏi đáp")
    user_question = st.text_input("Nhập câu hỏi của bạn:")
    
    if st.button("📩 Gửi câu hỏi"):
        if user_question:
            with st.spinner("Đang tìm câu trả lời..."):
                response = qa_chain.invoke({"query": user_question})
                st.write("🧠 **Câu trả lời:**")
                st.success(response)
        else:
            st.warning("⚠️ Vui lòng nhập câu hỏi.")
