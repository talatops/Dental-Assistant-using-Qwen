from ..conversation.manager import ConversationManager


def test_start_and_single_turn():
    manager = ConversationManager()
    conv_id, stream = manager.handle_turn(conversation_id=None, user_text="Hello, I want to book a check-up.")

    assert conv_id is not None
    # Consume the stream to ensure no errors are raised.
    text = "".join(list(stream))
    assert isinstance(text, str)

