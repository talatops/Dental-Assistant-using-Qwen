import { useState, type KeyboardEventHandler } from "react";

type Props = {
  disabled: boolean;
  onSend: (text: string) => void;
  onReset: () => void;
  isStreaming: boolean;
};

export function InputBox({ disabled, onSend, onReset, isStreaming }: Props) {
  const [value, setValue] = useState("");

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue("");
  };

  const handleKeyDown: KeyboardEventHandler<HTMLTextAreaElement> = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div
      style={{
        borderTop: "1px solid #e5e7eb",
        padding: "0.75rem 0.9rem",
        display: "flex",
        flexDirection: "column",
        gap: "0.5rem",
        backgroundColor: "#f9fafb",
        borderBottomLeftRadius: "1rem",
        borderBottomRightRadius: "1rem",
        overflow: "hidden",
      }}
    >
      <textarea
        rows={2}
        style={{
          width: "100%",
          boxSizing: "border-box",
          resize: "none",
          borderRadius: "0.9rem",
          border: "1px solid #d1d5db",
          padding: "0.55rem 0.9rem",
          fontSize: "0.95rem",
          outline: "none",
          boxShadow: "0 1px 2px rgba(15,23,42,0.06)",
        }}
        placeholder="Type your message and press Enter..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
      />
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "0.5rem" }}>
        <button
          type="button"
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          style={{
            padding: "0.5rem 1rem",
            borderRadius: "999px",
            border: "none",
            backgroundColor: disabled || !value.trim() ? "#9ca3af" : "#2563eb",
            color: "#ffffff",
            fontWeight: 500,
            cursor: disabled || !value.trim() ? "not-allowed" : "pointer",
          }}
        >
          Send
        </button>
        <button
          type="button"
          onClick={onReset}
          style={{
            padding: "0.4rem 0.9rem",
            borderRadius: "999px",
            border: "1px solid #d1d5db",
            backgroundColor: "#ffffff",
            color: "#111827",
            fontSize: "0.85rem",
            cursor: "pointer",
          }}
        >
          New session
        </button>
        {isStreaming && <span style={{ fontSize: "0.85rem", color: "#6b7280" }}>Assistant is typing…</span>}
      </div>
    </div>
  );
}

