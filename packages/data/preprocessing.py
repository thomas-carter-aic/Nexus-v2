"""
General text preprocessing utilities.
Lowercasing, whitespace cleanup, tokenization hooks.
"""

import re

def clean_text(text: str, lowercase: bool = True):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    if lowercase:
        text = text.lower()
    return text
