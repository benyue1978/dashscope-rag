# DeepSeek RAG 最小后端（Dashscope 版）

## 依赖环境

- Python 3.8+
- venv 虚拟环境

## 安装依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 配置环境变量

复制 `.env.example` 为 `.env`，填写 Dashscope API Key：

```bash
cp .env.example .env
# 编辑 .env，填写 DASHSCOPE_API_KEY
```

## PDF 嵌入命令

将 PDF 文件放入 data 目录，执行：

```bash
python embedding.py ../data/你的文件.pdf
```

## 启动 FastAPI 服务

```bash
uvicorn main:app --reload
```

## 问答接口

POST `/chat`

```json
{
  "user_query": "你的问题"
}
```

返回：

```json
{
  "answer": "模型回答",
  "references": ["相关段落1", "相关段落2", ...]
}
```

```shell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"user_query": "鸿沟是什么？"}'
```
