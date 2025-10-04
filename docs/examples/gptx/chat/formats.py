"""
Formatting utilities for chat datasets
"""

def chat_to_input_ids(chat_history, tokenizer):
    """
    Flatten chat history to input_ids
    chat_history: list of dicts {"role": "user/assistant", "content": str}
    """
    input_ids = []
    for msg in chat_history:
        input_ids.extend([ord(c) % 50257 for c in msg["content"]])
    return input_ids
