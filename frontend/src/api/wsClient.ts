export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

type IncomingFrame =
  | { type: "start"; conversation_id: string }
  | { type: "token"; token: string }
  | { type: "end"; latency: number; tokens: number }
  | { type: "error"; message: string };

export class ChatWebSocketClient {
  private socket: WebSocket | null = null;
  private backendUrl: string;
  private conversationId: string | null = null;

  constructor(backendWsUrl: string) {
    this.backendUrl = backendWsUrl;
  }

  connect(onFrame: (frame: IncomingFrame) => void, onClose: () => void, onError: (err: Event) => void) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return;
    }

    this.socket = new WebSocket(this.backendUrl);

    this.socket.onopen = () => {
      // Connection established
    };

    this.socket.onmessage = (event) => {
      try {
        const frame = JSON.parse(event.data) as IncomingFrame;
        if (frame.type === "start") {
          this.conversationId = frame.conversation_id;
        }
        onFrame(frame);
      } catch {
        // Ignore malformed frames
      }
    };

    this.socket.onclose = () => {
      onClose();
    };

    this.socket.onerror = (err) => {
      onError(err);
    };
  }

  sendMessage(message: string) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      throw new Error("WebSocket is not connected");
    }
    const payload = {
      conversation_id: this.conversationId,
      message,
    };
    this.socket.send(JSON.stringify(payload));
  }

  resetConversation() {
    this.conversationId = null;
  }
}

