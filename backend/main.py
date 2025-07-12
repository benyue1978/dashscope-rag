import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from dotenv import load_dotenv
from retrieval import retrieve_top_k
from chat import chat_with_context

# 依赖说明：
# - fastapi
# - pydantic
# - python-dotenv
# - retrieval.py, chat.py

load_dotenv()

logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境可用 *，生产建议指定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_query: str

class ChatResponse(BaseModel):
    answer: str
    references: List[str]

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest) -> ChatResponse:
    try:
        top_chunks = retrieve_top_k(req.user_query, k=5)
        if not top_chunks:
            raise HTTPException(status_code=404, detail="未检索到相关内容")
        contexts = [c[0] for c in top_chunks]
        answer = chat_with_context(contexts, req.user_query)
        # 只返回原始文档文件名，去重
        references = list({os.path.basename(c[1]["source"]) for c in top_chunks})
        return ChatResponse(answer=answer, references=references)
    except Exception as e:
        logger.error(f"Error in /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 