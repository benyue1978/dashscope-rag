import axios from "axios";

/**
 * 向后端 /chat 接口发送请求
 * @param user_query - 用户问题
 * @returns 后端响应数据
 */
export async function postChat(user_query: string) {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE || "";
  const res = await axios.post(`${baseUrl}/chat`, { user_query });
  return res.data;
} 