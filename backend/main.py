from __future__ import annotations

import asyncio
import json
import time
from typing import Any, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from .conversation.manager import ConversationManager


app = FastAPI(title="Dental Clinic Conversational Assistant")

conversation_manager = ConversationManager()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/test-dialogue")
async def test_dialogue(payload: Dict[str, Any]) -> JSONResponse:
    """
    Simple non-streaming endpoint for testing via Postman.
    Expects JSON: { "conversation_id": string | null, "message": string }
    """
    conversation_id = payload.get("conversation_id")
    message = payload.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return JSONResponse({"error": "message must be a non-empty string"}, status_code=400)

    conversation_id, stream = conversation_manager.handle_turn(conversation_id, message)
    full_text = "".join(list(stream))
    return JSONResponse({"conversation_id": conversation_id, "response": full_text})


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for real-time streaming chat.

    Protocol:
      - Client sends JSON: { "conversation_id": string | null, "message": string }
      - Server replies:
          { "type": "start", "conversation_id": "..." }
          { "type": "token", "token": "..." }  # repeated
          { "type": "end", "latency": float, "tokens": int }
        or
          { "type": "error", "message": "..." }
    """
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON payload"})
                continue

            conversation_id = payload.get("conversation_id")
            message = payload.get("message", "")

            if not isinstance(message, str) or not message.strip():
                await websocket.send_json({"type": "error", "message": "message must be a non-empty string"})
                continue

            start_time = time.time()
            conversation_id, stream = conversation_manager.handle_turn(conversation_id, message)
            await websocket.send_json({"type": "start", "conversation_id": conversation_id})

            token_count = 0
            try:
                for token in stream:
                    token_count += 1
                    await websocket.send_json({"type": "token", "token": token})
                    # Allow other tasks to run
                    await asyncio.sleep(0)
            except Exception as exc:  # noqa: BLE001
                await websocket.send_json({"type": "error", "message": f"generation error: {exc}"})
                continue

            latency = time.time() - start_time
            await websocket.send_json({"type": "end", "latency": latency, "tokens": token_count})

    except WebSocketDisconnect:
        # Client disconnected; nothing special to clean up for in-memory state.
        return

