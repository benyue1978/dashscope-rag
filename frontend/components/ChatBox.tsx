"use client";

import { useState } from "react";
import { postChat } from "../lib/api";
import clsx from "clsx";

/**
 * ChatBox 组件：输入 content 和 user_query，调用 /chat 接口，展示结果和引用。
 * 无 props，内部管理状态。
 */
export default function ChatBox() {
  const [userQuery, setUserQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [references, setReferences] = useState<string[]>([]);

  const handleSend = async () => {
    setError("");
    if (!userQuery.trim()) {
      setError("问题不能为空");
      return;
    }
    setLoading(true);
    try {
      const data = await postChat(userQuery);
      setResult(data.answer || "无返回结果");
      setReferences(data.references || []);
    } catch (e: any) {
      setError(e?.message || "请求失败");
      setResult(null);
      setReferences([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-2">
      <div className="w-full max-w-2xl bg-white/90 rounded-3xl shadow-2xl p-8 flex flex-col gap-8 border border-gray-100">
        <div className="flex flex-col gap-4">
          <input
            className="border border-gray-300 rounded-xl p-4 text-lg focus:outline-none focus:ring-2 focus:ring-blue-200 transition min-h-[48px] bg-gray-50 placeholder-gray-500 text-gray-900"
            placeholder="请输入你的问题..."
            value={userQuery}
            onChange={e => setUserQuery(e.target.value)}
            maxLength={200}
            disabled={loading}
            onKeyDown={e => { if (e.key === 'Enter' && !loading) handleSend(); }}
          />
        </div>
        <button
          className={clsx(
            "bg-black text-white rounded-xl px-6 py-3 text-lg font-bold shadow-md transition-all duration-150 active:scale-95 hover:bg-gray-900 disabled:opacity-60 disabled:cursor-not-allowed",
            loading && "animate-pulse"
          )}
          onClick={handleSend}
          disabled={loading || !userQuery.trim()}
        >
          {loading ? (
            <span className="flex items-center gap-2 justify-center">
              <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" /></svg>
              发送中...
            </span>
          ) : "发送"}
        </button>
        {error && <div className="text-red-500 text-base text-center bg-red-50 rounded-lg py-2 px-4 border border-red-100">{error}</div>}
        {result && (
          <div className="bg-gray-50 rounded-2xl p-6 whitespace-pre-wrap text-gray-800 shadow-inner border border-gray-100">
            <div className="font-bold mb-2 text-lg text-gray-700">回答：</div>
            <div className="text-base leading-relaxed">{result}</div>
          </div>
        )}
        {references.length > 0 && (
          <div className="bg-gray-100 rounded-2xl p-5 shadow-inner border border-gray-200">
            <div className="font-bold mb-2 text-gray-700">引用：</div>
            <ul className="list-disc list-inside text-base text-gray-600 space-y-1">
              {references.map((ref, i) => (
                <li key={i} className="bg-white/80 rounded px-3 py-1 inline-block shadow-sm border border-gray-50">{ref}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
} 