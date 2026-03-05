from __future__ import annotations

import uuid
from typing import Generator

from ..llm.client import LLMClient, GenerationConfig
from .memory import ConversationMemory, Message
from . import prompts


class ConversationManager:
    """
    Orchestrates multi-turn conversations for the dental clinic assistant.
    """

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self._memory = ConversationMemory()
        self._llm = llm_client or LLMClient()

    def start_conversation(self, user_metadata: dict | None = None) -> str:
        """
        Initialize a new conversation and return its ID.
        """
        conversation_id = str(uuid.uuid4())
        system_prompt = prompts.get_system_prompt()
        self._memory.append(conversation_id, Message(role="system", content=system_prompt))
        # Optionally store metadata as a special message
        if user_metadata:
            meta_text = f"[metadata] {user_metadata}"
            self._memory.append(conversation_id, Message(role="system", content=meta_text))
        return conversation_id

    def add_user_message(self, conversation_id: str, text: str) -> None:
        self._memory.append(conversation_id, Message(role="user", content=text))

    def build_prompt(self, conversation_id: str) -> str:
        history_dicts = self._memory.as_dicts(conversation_id)
        return prompts.build_prompt(history_dicts)

    def handle_turn(self, conversation_id: str | None, user_text: str) -> tuple[str, Generator[str, None, None]]:
        """
        Process a single user turn.

        Returns:
          - conversation_id (new or existing)
          - generator that yields assistant tokens
        """
        created_new = False
        if not conversation_id:
            conversation_id = self.start_conversation(user_metadata=None)
            created_new = True

        self.add_user_message(conversation_id, user_text)
        prompt = self.build_prompt(conversation_id)

        gen_config = GenerationConfig()
        stream = self._llm.generate_stream(prompt, gen_config=gen_config)

        def _stream_with_memory() -> Generator[str, None, None]:
            """
            Stream tokens to the client while also building the full response.
            If the model starts emitting another \"User:\" or \"Assistant:\" turn,
            we stop streaming and discard everything after that marker so that
            each response is a single assistant message.
            """
            response_chunks: list[str] = []
            buffer = ""
            stop_markers = ["\nUser:", "\nAssistant:", "User:", "Assistant:"]

            for token in stream:
                # Tentatively extend the buffer with this token.
                next_buffer = buffer + token
                cut_index = None
                for marker in stop_markers:
                    idx = next_buffer.find(marker)
                    if idx != -1:
                        cut_index = idx
                        break

                if cut_index is not None:
                    # Finalize buffer up to the marker and stop streaming.
                    buffer = next_buffer[:cut_index]
                    break

                # No marker detected, so we accept this token.
                buffer = next_buffer
                response_chunks.append(token)
                yield token

            full_response = buffer.strip()
            if full_response:
                self._memory.append(conversation_id, Message(role="assistant", content=full_response))

        return conversation_id, _stream_with_memory()

