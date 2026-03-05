import { useEffect, useMemo, useState } from "react";
import { ChatWebSocketClient, type ChatMessage } from "./api/wsClient";
import { MessageList } from "./components/MessageList";
import { InputBox } from "./components/InputBox";

const DEFAULT_WS_URL = import.meta.env.VITE_BACKEND_WS_URL ?? "ws://localhost:8000/ws/chat";

function cleanAssistantText(raw: string): string {
  let text = raw;

  // Cut off any extra simulated turns.
  const markers = ["\nUser:", "\nAssistant:", "User:", "Assistant:"];
  for (const marker of markers) {
    const idx = text.indexOf(marker);
    if (idx !== -1) {
      text = text.slice(0, idx);
      break;
    }
  }

  // Trim trailing standalone "User" token if it slipped through.
  text = text.trimEnd();
  if (text.endsWith("User")) {
    text = text.slice(0, -4);
  }

  return text.trim();
}

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [connected, setConnected] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentAssistantBuffer, setCurrentAssistantBuffer] = useState<string | null>(null);

  const client = useMemo(() => new ChatWebSocketClient(DEFAULT_WS_URL), []);

  useEffect(() => {
    client.connect(
      (frame) => {
        if (frame.type === "start") {
          setIsStreaming(true);
          setCurrentAssistantBuffer("");
        } else if (frame.type === "token") {
          setCurrentAssistantBuffer((prev) => (prev ?? "") + frame.token);
        } else if (frame.type === "end") {
          setIsStreaming(false);
          // Use the latest buffer value when the end frame arrives, and clean it.
          setCurrentAssistantBuffer((finalBuffer) => {
            const cleaned = cleanAssistantText(finalBuffer ?? "");
            if (cleaned) {
              setMessages((prev) => [...prev, { role: "assistant", content: cleaned }]);
            }
            return null;
          });
        } else if (frame.type === "error") {
          setError(frame.message);
          setIsStreaming(false);
        }
      },
      () => {
        setConnected(false);
      },
      () => {
        setError("WebSocket connection error.");
      },
    );
    setConnected(true);
  }, [client]);

  const handleSend = (text: string) => {
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setError(null);
    try {
      client.sendMessage(text);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unable to send message.");
    }
  };

  const handleReset = () => {
    client.resetConversation();
    setMessages([]);
    setCurrentAssistantBuffer(null);
    setError(null);
  };

  const allMessages = currentAssistantBuffer
    ? [...messages, { role: "assistant" as const, content: currentAssistantBuffer }]
    : messages;

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "stretch",
        justifyContent: "center",
        backgroundColor: "#f3f4f6",
        padding: "0",
        fontFamily: "-apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      }}
    >
      {/* Top app bar */}
      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          height: "56px",
          background: "linear-gradient(to right, #2563eb, #38bdf8)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 1.75rem",
          boxShadow: "0 4px 10px rgba(15,23,42,0.25)",
          zIndex: 20,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <div
            style={{
              width: 32,
              height: 32,
              borderRadius: "999px",
              backgroundColor: "rgba(239,246,255,0.15)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#eff6ff",
              fontWeight: 600,
              fontSize: "0.85rem",
            }}
          >
            DC
          </div>
          <div>
            <div style={{ color: "#eff6ff", fontWeight: 600, fontSize: "0.95rem" }}>Dental Clinic Assistant</div>
            <div style={{ color: "#dbeafe", fontSize: "0.8rem" }}>Smart appointment helper for your patients</div>
          </div>
        </div>
        <span
          style={{
            fontSize: "0.8rem",
            padding: "0.25rem 0.8rem",
            borderRadius: "999px",
            backgroundColor: connected ? "rgba(187,247,208,0.25)" : "rgba(254,202,202,0.25)",
            color: connected ? "#bbf7d0" : "#fee2e2",
            border: "1px solid rgba(209,250,229,0.5)",
          }}
        >
          {connected ? "Connected" : "Disconnected"}
        </span>
      </div>

      {/* Main content area */}
      <div
        style={{
          marginTop: "72px",
          padding: "1.5rem",
          width: "100%",
          maxWidth: "960px",
          marginInline: "auto",
        }}
      >
        {/* Chat panel (centered card) */}
        <div
          style={{
            backgroundColor: "#ffffff",
            borderRadius: "1rem",
            boxShadow: "0 18px 45px rgba(15,23,42,0.18)",
            display: "flex",
            flexDirection: "column",
            border: "1px solid #e5e7eb",
            minHeight: "60vh",
          }}
        >
          <header
            style={{
              padding: "0.85rem 1rem",
              borderBottom: "1px solid #e5e7eb",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              backgroundColor: "#f9fafb",
              borderTopLeftRadius: "1rem",
              borderTopRightRadius: "1rem",
            }}
          >
            <div>
              <h2 style={{ fontSize: "1rem", fontWeight: 600, color: "#111827" }}>Chat</h2>
              <p style={{ fontSize: "0.8rem", color: "#6b7280" }}>
                Describe your dental concern or request an appointment.
              </p>
            </div>
          </header>
          <MessageList messages={allMessages} />
          {error && (
            <div
              style={{
                color: "#b91c1c",
                backgroundColor: "#fee2e2",
                padding: "0.5rem 1rem",
                fontSize: "0.85rem",
                borderTop: "1px solid #fecaca",
              }}
            >
              {error}
            </div>
          )}
          <InputBox disabled={!connected} onSend={handleSend} onReset={handleReset} isStreaming={isStreaming} />
        </div>
      </div>
    </div>
  );
}

export default App;

