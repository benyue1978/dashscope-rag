import os
from typing import List, Tuple
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from openai import OpenAI

# 依赖说明：
# - chromadb==1.0.15
# - openai>=1.2.0
# - python-dotenv

load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_DB_DIR, settings=Settings(allow_reset=True))
collection = client.get_or_create_collection("rag_docs")

openai_client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def embed_query(query: str) -> List[float]:
    """
    将用户问题转为向量。
    """
    response = openai_client.embeddings.create(
        input=[query],
        model="text-embedding-v1"
    )
    return response.data[0].embedding

def retrieve_top_k(query: str, k: int = 5) -> List[Tuple[str, dict]]:
    """
    检索 top_k 最相关段落。
    返回 [(段落文本, metadata), ...]
    """
    query_vec = embed_query(query)
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=k,
        include=["documents", "metadatas"]
    )
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    print("Collection count:", collection.count())  # 临时调试用
    return list(zip(docs, metas)) 