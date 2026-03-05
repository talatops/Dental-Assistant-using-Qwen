import type { ChatMessage } from "../api/wsClient";

type Props = {
  messages: ChatMessage[];
};

export function MessageList({ messages }: Props) {
  return (
    <div
      style={{
        flex: 1,
        overflowY: "auto",
        padding: "1rem",
        display: "flex",
        flexDirection: "column",
        gap: "0.75rem",
        backgroundColor: "#f9fafb",
        borderTop: "1px solid #e5e7eb",
        borderBottom: "1px solid #e5e7eb",
      }}
    >
      {messages.map((msg, idx) => (
        <div
          key={idx}
          style={{
            alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
            maxWidth: "80%",
            padding: "0.75rem 1rem",
            borderRadius: "1.25rem",
            backgroundColor: msg.role === "user" ? "#2563eb" : "#e5e7eb",
            color: msg.role === "user" ? "#ffffff" : "#111827",
            fontSize: "0.95rem",
            boxShadow: msg.role === "user" ? "0 4px 10px rgba(37,99,235,0.35)" : "0 3px 8px rgba(15,23,42,0.18)",
          }}
        >
          {msg.content}
        </div>
      ))}
    </div>
  );
}

