## 🔥 Giới thiệu
Dự án này là một chatbot hỏi đáp sử dụng LangChain, FAISS và Mistral AI để tạo cơ sở dữ liệu vector và thực hiện tìm kiếm ngữ nghĩa.

## 🛠 Cài Đặt
### 1. Clone Repository
```sh
git clone https://github.com/vinz0369/humgask_rag_chatbot
```

### 2. Tạo Virtual Environment (Tùy chọn)
```sh
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate    # Trên Windows
```

### 3. Cài Đặt Dependencies
```sh
pip install -r requirements.txt
```

### 4. Cấu Hình API Key
Tạo một file `.env` trong thư mục gốc và thêm API Key của Mistral AI:
```sh
MISTRAL_API_KEY=your_api_key_here
```

## 🚀 Cách Chạy Dự Án
```sh
streamlit run app.py
```

## 📂 Cấu Trúc Dự Án
```
📂 pdf-chatbot
├── 📂 data              
├── 📂 vectorstores        
├── prepare_vector_db.py                
├── qna_ui.py               
├── requirements.txt      
└── README.md            
```



