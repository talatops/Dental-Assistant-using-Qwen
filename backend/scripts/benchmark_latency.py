import time
from typing import List

import requests


PROMPTS: List[str] = [
    "You are a helpful dental clinic assistant. Briefly introduce yourself.",
    "A patient wants to book a routine dental check-up. Respond concisely and ask for missing details.",
    "Explain, in simple terms, what a routine dental cleaning involves. Keep it under 5 sentences.",
]


def run_benchmarks() -> None:
    for i, prompt in enumerate(PROMPTS, start=1):
        print(f"=== Prompt {i} ===")
        print(prompt)

        start_time = time.time()
        resp = requests.post(
            "http://localhost:8000/test-dialogue",
            json={"conversation_id": None, "message": prompt},
            timeout=120,
        )
        end_time = time.time()

        total_time = end_time - start_time
        if resp.status_code != 200:
            print(f"Request failed with status {resp.status_code}: {resp.text}")
            print()
            continue

        data = resp.json()
        text = data.get("response", "")
        token_count = len(text.split())
        tokens_per_second = token_count / max(total_time, 1e-6)

        print(f"Total time: {total_time:.3f}s")
        print(f"Tokens generated (approx words): {token_count}")
        print(f"Tokens/sec (approx): {tokens_per_second:.2f}")
        print()


if __name__ == "__main__":
    run_benchmarks()

