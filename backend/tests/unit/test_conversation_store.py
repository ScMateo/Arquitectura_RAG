"""Unit tests for InMemoryConversationStore (HU-07)."""

from app.domain.entities.message import Message
from app.domain.value_objects.message_role import MessageRole
from app.infrastructure.conversation.in_memory_conversation_store import (
    InMemoryConversationStore,
)


def _message(content: str) -> Message:
    return Message(role=MessageRole.USER, content=content)


def test_get_creates_conversation_on_demand() -> None:
    store = InMemoryConversationStore()
    conversation = store.get("s1")
    assert conversation.session_id == "s1"
    assert conversation.messages == []
    assert store.get("s1") is conversation


def test_add_message_appends_in_order() -> None:
    store = InMemoryConversationStore()
    store.add_message("s1", _message("a"))
    store.add_message("s1", _message("b"))
    assert [message.content for message in store.get("s1").messages] == ["a", "b"]


def test_history_window_is_bounded() -> None:
    store = InMemoryConversationStore(max_history=5)
    for index in range(7):
        store.add_message("s1", _message(f"m{index}"))
    messages = store.get("s1").messages
    assert len(messages) == 5
    assert [message.content for message in messages] == ["m2", "m3", "m4", "m5", "m6"]


def test_sessions_are_isolated() -> None:
    store = InMemoryConversationStore()
    store.add_message("a", _message("para-a"))
    store.add_message("b", _message("para-b"))
    assert [message.content for message in store.get("a").messages] == ["para-a"]
    assert [message.content for message in store.get("b").messages] == ["para-b"]


def test_clear_removes_session() -> None:
    store = InMemoryConversationStore()
    store.add_message("s1", _message("a"))
    store.clear("s1")
    assert store.get("s1").messages == []
