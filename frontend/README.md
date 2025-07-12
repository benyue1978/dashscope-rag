
---

# DashScope RAG 前端

本项目为 DashScope RAG 系统的 Next.js 前端，基于 App Router + Tailwind CSS + Axios。

## 环境变量配置
- 在 `frontend/.env.local` 文件中添加：
  ```env
  NEXT_PUBLIC_API_BASE=http://localhost:8000
  ```
- 生产环境请填写实际后端服务地址。

## 目录结构
- `app/`：页面文件（App Router）
- `components/`：通用 UI 组件
- `lib/`：API 封装等工具

## 启动开发

```bash
cd frontend
npm install
npm run dev
```

浏览器访问 [http://localhost:3000](http://localhost:3000)

## 主要依赖
- next
- react
- tailwindcss
- axios
- classnames/clsx
- @headlessui/react

## 与后端接口约定
- POST `/chat`，参数：`content`、`user_query`
- 返回：`{ answer: string, references: string[] }`

## 代码风格
- 组件命名 PascalCase，文件 kebab-case
- 逻辑与展示分层，详见 `components/ChatBox.tsx`

---
