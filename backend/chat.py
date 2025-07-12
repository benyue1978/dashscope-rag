import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import logging

# 依赖说明：
# - openai>=1.2.0
# - python-dotenv
# - logging（标准库）

load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

openai_client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

logger = logging.getLogger("chat")
logging.basicConfig(level=logging.INFO)

def build_prompt(contexts: List[str], user_query: str) -> str:
    """
    拼接 context 和用户问题。
    """
    context_str = "\n\n".join(contexts)
    prompt = f"请根据以下内容回答问题：\n\n{context_str}\n\n问题：{user_query}\n\n答案："
    return prompt

def chat_with_context(contexts: List[str], user_query: str) -> str:
    """
    用 qwen-turbo-latest 生成回答。
    """
    prompt = build_prompt(contexts, user_query)
    logger.info(f"Prompt: {prompt[:200]}...")
    response = openai_client.chat.completions.create(
        model="qwen-turbo-latest",
        messages=[
            {"role": "system", "content": "你是一个专业的中文智能问答助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip() 