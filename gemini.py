import os
from config import api_key
from flask import Flask, request, jsonify

from langchain_qdrant import QdrantVectorStore
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import CSVLoader
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
#import pandas as pd
#from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)

# 讀取 CSV 檔案
loader = CSVLoader(file_path=資訊問題題庫-改善.csv)
data = loader.load()
#df = pd.DataFrame(data)

# 設定嵌入模型
persist_directory = 'db'
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'}
embedding = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

# 設定 Qdrant 向量存儲
qdrant = QdrantVectorStore.from_documents(
    data,
    embedding,
    location=":memory:",
    collection_name="my_documents",
)

# 設定 GROQ AI
os.environ["GROQ_API_KEY"] 
llm = ChatGroq(model='llama3-70b-8192',temperature=0)
response = llm.invoke('你好')
print(response.content)

# 設定Prompt模板
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "你是電腦資訊專家以及站務客服人員，請協助回答電腦資訊相關問題以及回答捷運相關問題,\
        其他不相關的問題請回答不知道,\
        請你根據問題查詢文件後回答，請不要回答使用者問題\
        並根據'小建議'、'參考來源'、'所屬類別'這樣的順序回答\
        '小建議'請根據'簡易故障排除'以及'可能原因'綜合這兩個項目生成回答\
        '參考來源'請從提供該文件的名字，以支持您的回答，如果問題不在提供的文件中就自行去網路檢索並回答"
        ),
    # context 和 question 為 RetrievalQA 的固定用法
    HumanMessagePromptTemplate.from_template(
        "使用繁體中文回答，回答時要提供'小建議'、'參考來源文件的名字'及'所屬類別'，\
        如果問題不在提供的文件中就自行去網路檢索並回答，並提供參考的網路連結"
        "Q:{query},參考文件:{source_documents}")
])

# 自定義預處理函數
def custom_preprocess_func(query):
    if isinstance(query, dict):
        return query.get("query", "").split()  # 確保取出 query 並進行處理
    return query.split()

# 設定檢索器
bm25_retriever = BM25Retriever.from_documents(data, preprocess_func=custom_preprocess_func)
bm25_retriever.k = 7

faiss_retriever = qdrant.as_retriever()

# 使用 EnsembleRetriever 來結合檢索器
ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5])

# 設定 chain
chain = (
    {"context": ensemble_retriever, "query": RunnablePassthrough(), 
     "source_documents": ensemble_retriever, "class": ensemble_retriever} 
    | prompt
    | llm
    | StrOutputParser()
)

def extract_category(text):
    lines = text.split("\n")
    category = None

    for i, line in enumerate(lines):
        if "**所屬類別**" in line:
            # 嘗試在同一行中提取
            if "**" in line:
                potential_category = line.split("*", 4)[1].strip().strip("* ").strip()
                if potential_category and not potential_category.startswith("{"):
                    category = potential_category
                    break
            # 如果內容在下一行，則提取下一行的內容
            if i + 1 < len(lines):
                potential_category = lines[i + 1].strip("* ").strip()
                if potential_category and not potential_category.startswith("{"):
                    category = potential_category
                    break
    return category

# 定義 API 路由
@app.route('/ask', methods=['POST'])
def ask_question():
    # 获取用户输入
    user_input = request.json.get('question')
    if not user_input:
        return jsonify({"error": "請提供問題"}), 400

    print(f"用戶查詢: {user_input}")

    # 調用鏈
    # 注意這裡直接傳遞user_input字串，而不是將其放在字典中
    question=user_input
    response = chain.invoke(question)
    print(response) 
    answer = response

    # 提取類別
    category1 = extract_category(answer)
    print(category1)

    doc1=ensemble_retriever.invoke(question)
    print(doc1)
    # 判斷回答類型
    answer_type = "基於文件回答" if doc1 else "自行生成的回答"
    
# 將 doc1 轉換為可序列化的格式，並將 set 轉換為 list
    doc1_serialized = [
        {
            'page_content': doc.page_content,
            'metadata': {key: list(value) if isinstance(value, set) else value 
                          for key, value in doc.metadata.items()}
        } 
        for doc in doc1
    ]

    # 返回所有相關資訊，包括序列化的 doc1
    return jsonify({
        "user_input": user_input,
        "answer": answer,
        "answer_type": answer_type,
        "category": category1,
        "doc1": doc1_serialized, 
    })

if __name__ == '__main__':
    app.run(debug=True)
