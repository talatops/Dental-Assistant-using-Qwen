from __future__ import annotations

from dataclasses import dataclass
from typing import Generator, Iterable

from llama_cpp import Llama

from .. import config


@dataclass
class GenerationConfig:
    max_new_tokens: int = config.MAX_NEW_TOKENS
    temperature: float = config.TEMPERATURE
    top_p: float = config.TOP_P
    top_k: int = config.TOP_K


class LLMClient:
    """
    Thin abstraction over the local Qwen model runtime using llama-cpp-python.

    This loads the Qwen2-0.5B-Instruct-GGUF model via `Llama.from_pretrained`,
    so inference runs fully locally on CPU.
    """

    def __init__(self, model_path: str | None = None) -> None:
        # You can optionally pass a local GGUF path via model_path and use it
        # instead of from_pretrained if you want full offline control.
        self.model_path = str(model_path or config.MODEL_PATH)

        self._engine = Llama.from_pretrained(
            repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
            filename="qwen2-0_5b-instruct-fp16.gguf",
            n_ctx=config.CONTEXT_WINDOW_TOKENS,
            verbose=False,
        )

    def generate_stream(self, prompt: str, gen_config: GenerationConfig | None = None) -> Generator[str, None, None]:
        """
        Stream tokens from the local model for the given prompt.
        """
        if gen_config is None:
            gen_config = GenerationConfig()

        stream = self._engine.create_completion(
            prompt=prompt,
            max_tokens=gen_config.max_new_tokens,
            temperature=gen_config.temperature,
            top_p=gen_config.top_p,
            top_k=gen_config.top_k,
            stream=True,
        )

        for chunk in stream:
            text = chunk["choices"][0]["text"]
            if text:
                yield text

    def generate(self, prompt: str, gen_config: GenerationConfig | None = None) -> str:
        """
        Convenience non-streaming wrapper that joins the streamed tokens.
        """
        return "".join(self.generate_stream(prompt, gen_config=gen_config))


def benchmark_prompts(client: LLMClient, prompts: Iterable[str]) -> None:
    """
    Simple benchmarking helper used by the benchmark script.
    Measures time to first token and total generation time per prompt.
    The detailed timing is implemented in the benchmark script itself.
    """
    for prompt in prompts:
        # The benchmark script will wrap this call with timing logic.
        for _ in client.generate_stream(prompt):
            break

