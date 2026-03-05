import asyncio
import json
import time
from typing import Any

import websockets


WS_URL = "ws://localhost:8000/ws/chat"


async def run_single_client(index: int) -> float:
    """
    Run a single WebSocket client and return the total time for one request.
    """
    start = time.time()
    async with websockets.connect(WS_URL) as ws:
        payload = {"conversation_id": None, "message": f"Hello, I am test client {index}. I want to book a check-up."}
        await ws.send(json.dumps(payload))

        async for message in ws:
            frame: dict[str, Any] = json.loads(message)
            if frame.get("type") == "end":
                break
    end = time.time()
    return end - start


async def main() -> None:
    clients = 5
    tasks = [asyncio.create_task(run_single_client(i)) for i in range(clients)]
    durations = await asyncio.gather(*tasks)

    avg = sum(durations) / len(durations)
    print(f"Ran {clients} concurrent WebSocket clients.")
    print("Per-client total times (s):", ", ".join(f"{d:.3f}" for d in durations))
    print(f"Average total time per client: {avg:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())

