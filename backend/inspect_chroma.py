import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

load_dotenv()

CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "chroma_db")
client = chromadb.PersistentClient(path=CHROMA_DB_DIR, settings=Settings(allow_reset=True))
collection = client.get_or_create_collection("rag_docs")

print("Collection count:", collection.count())

results = collection.get(include=["documents", "metadatas"])
max_show = 10
for i, doc in enumerate(results["documents"][:max_show]):
    print(f"--- 文档 {i+1} ---")
    print("ID:", results["ids"][i])
    print("内容:", doc)
    print("元数据:", results["metadatas"][i])
    print()
if collection.count() > max_show:
    print(f"... 仅显示前 {max_show} 条，共 {collection.count()} 条 ...") 