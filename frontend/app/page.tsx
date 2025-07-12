import ChatBox from "../components/ChatBox";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
      <h1 className="text-4xl font-extrabold mb-8 text-gray-900 drop-shadow-sm tracking-tight">DashScope RAG Demo</h1>
      <ChatBox />
    </main>
  );
}
