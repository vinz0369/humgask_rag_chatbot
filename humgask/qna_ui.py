import streamlit as st
from chat import answer_question, create_or_update_db

# Tạo giao diện Streamlit
st.set_page_config(page_title="Chatbot Hỏi Đáp PDF", layout="wide")

st.title("📄 Chatbot Hỏi Đáp từ Tài Liệu PDF")

# Tạo sidebar để quản lý dữ liệu
with st.sidebar:
    st.header("⚙️ Cấu hình")
    if st.button("🔄 Cập nhật dữ liệu từ PDF"):
        with st.spinner("Đang cập nhật dữ liệu..."):
            create_or_update_db()
        st.success("Dữ liệu đã được cập nhật thành công!")

# Ô nhập câu hỏi
question = st.text_input("Nhập câu hỏi của bạn:", "")

# Nếu người dùng nhập câu hỏi, gọi chatbot
if question:
    with st.spinner("Đang tìm kiếm câu trả lời..."):
        response = answer_question(question)
    st.subheader("💬 Trả lời:")
    st.write(response)
