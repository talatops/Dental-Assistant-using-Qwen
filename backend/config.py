from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

# Path to the local quantized Qwen model (GGUF or similar)
MODEL_PATH = BASE_DIR.parent / "models" / "qwen" / "qwen-small-q4_k.gguf"

# Inference parameters tuned for CPU-only latency
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.7
TOP_P = 0.9
TOP_K = 40

# Approximate context window size (depends on the chosen model)
CONTEXT_WINDOW_TOKENS = 2048

# Streaming and timeout configuration
STREAM_CHUNK_SIZE = 8
INFERENCE_TIMEOUT_SECONDS = 60

