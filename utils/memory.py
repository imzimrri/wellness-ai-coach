import json
import os
import streamlit as st
from typing import List, Dict, Any

MEMORY_FILE = "data/memory.json"

class MemoryBank:
    """
    Manages long-term memory persistence using a JSON file.
    Stores user facts and preferences that persist across sessions.
    """
    def __init__(self):
        self.memory_file = MEMORY_FILE
        self._ensure_memory_file()

    def _ensure_memory_file(self):
        """Ensures the memory file and directory exist."""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as f:
                json.dump({}, f)

    def load_memory(self) -> Dict[str, Any]:
        """Loads the entire memory bank."""
        try:
            with open(self.memory_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_memory(self, memory: Dict[str, Any]):
        """Saves the entire memory bank."""
        with open(self.memory_file, "w") as f:
            json.dump(memory, f, indent=2)

    def get_fact(self, key: str) -> Any:
        """Retrieves a specific fact."""
        memory = self.load_memory()
        return memory.get(key)

    def set_fact(self, key: str, value: Any):
        """Sets a specific fact and saves it."""
        memory = self.load_memory()
        memory[key] = value
        self.save_memory(memory)

    def clear_memory(self):
        """Clears all stored memory."""
        self.save_memory({})
        
    def get_all_memories_as_text(self) -> str:
        """Returns all memories formatted as a string for context injection."""
        memory = self.load_memory()
        if not memory:
            return "No long-term memories stored yet."
        
        text = "Long-term Memory:\n"
        for key, value in memory.items():
            text += f"- {key}: {value}\n"
        return text

class SessionManager:
    """
    Wraps Streamlit's session state to manage chat history and short-term context.
    """
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def add_message(self, role: str, content: str):
        """Adds a message to the session history."""
        st.session_state.messages.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        """Returns the full chat history."""
        return st.session_state.messages

    def get_recent_history(self, limit: int = 5) -> List[Dict[str, str]]:
        """Returns the last N messages for context."""
        return st.session_state.messages[-limit:]

    def clear_history(self):
        """Clears the chat history."""
        st.session_state.messages = []
