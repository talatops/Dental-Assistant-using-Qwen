from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Dict, List, Literal, Any

from .. import config


Role = Literal["system", "user", "assistant"]


@dataclass
class Message:
    role: Role
    content: str
    timestamp: float = field(default_factory=time)


class ConversationMemory:
    """
    Simple in-memory store mapping conversation_id -> list[Message].

    For the assignment, an in-process dictionary is sufficient. In a more
    advanced deployment, this could be swapped out for a database or cache.
    """

    def __init__(self) -> None:
        self._store: Dict[str, List[Message]] = {}

    def get_history(self, conversation_id: str) -> List[Message]:
        return self._store.get(conversation_id, [])

    def append(self, conversation_id: str, message: Message) -> None:
        history = self._store.setdefault(conversation_id, [])
        history.append(message)
        self._truncate_if_needed(conversation_id)

    def _truncate_if_needed(self, conversation_id: str) -> None:
        """
        Naive context window management based on character length.
        In a real system you would use token counts.
        """
        history = self._store.get(conversation_id, [])
        if not history:
            return

        max_chars = config.CONTEXT_WINDOW_TOKENS * 4  # rough approximation
        total_chars = sum(len(m.content) for m in history)

        if total_chars <= max_chars:
            return

        # Drop oldest user/assistant messages but keep the earliest system message if present.
        system_messages = [m for m in history if m.role == "system"]
        non_system = [m for m in history if m.role != "system"]

        # Always keep at least the earliest system message, if any.
        new_history: List[Message] = system_messages[:1]
        # Keep most recent non-system messages until within budget.
        running_chars = sum(len(m.content) for m in new_history)
        for msg in reversed(non_system):
            msg_len = len(msg.content)
            if running_chars + msg_len > max_chars:
                break
            new_history.insert(1, msg)
            running_chars += msg_len

        self._store[conversation_id] = new_history

    def as_dicts(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Export history as a list of dictionaries suitable for prompt building.
        """
        return [
            {"role": m.role, "content": m.content, "timestamp": m.timestamp}
            for m in self.get_history(conversation_id)
        ]

