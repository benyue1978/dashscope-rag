import os
import sys
from typing import List
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from unstructured.partition.pdf import partition_pdf
from openai import OpenAI
import logging

# 依赖说明：
# - chromadb==1.0.15
# - unstructured==0.16.24
# - openai>=1.2.0
# - python-dotenv
# - logging（标准库）

load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")

# 配置 ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DB_DIR, settings=Settings(allow_reset=True))
collection = client.get_or_create_collection("rag_docs")

# 配置 Dashscope embedding（兼容 OpenAI API）
openai_client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

logger = logging.getLogger("embedding")
logging.basicConfig(level=logging.INFO)

def pdf_to_chunks(pdf_path: str, chunk_size: int = 300) -> List[str]:
    """
    将 PDF 文件分段为文本块。
    """
    elements = partition_pdf(filename=pdf_path)
    text = "\n".join([el.text for el in elements if hasattr(el, "text") and el.text])
    # 简单按长度分段
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return [c.strip() for c in chunks if c.strip()]

def batch_iter(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i:i+batch_size]

def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    使用 Dashscope embedding 模型将文本转为向量，分批处理（每批最多25条）。
    """
    all_embeddings = []
    for batch in batch_iter(texts, 25):
        response = openai_client.embeddings.create(
            input=batch,
            model="text-embedding-v1"
        )
        all_embeddings.extend([d.embedding for d in response.data])
    return all_embeddings

def add_pdf_to_chroma(pdf_path: str):
    """
    处理 PDF，分段并嵌入，写入 ChromaDB。
    """
    logger.info(f"Processing PDF: {pdf_path}")
    chunks = pdf_to_chunks(pdf_path)
    logger.info(f"Total chunks: {len(chunks)}")
    embeddings = embed_texts(chunks)
    ids = [f"{os.path.basename(pdf_path)}_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source": pdf_path}] * len(chunks)
    )
    logger.info(f"Added {len(chunks)} chunks to ChromaDB.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python embedding.py <pdf_path>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    add_pdf_to_chroma(pdf_path) 