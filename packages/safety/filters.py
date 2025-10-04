"""
Safety filters for mini-GPT outputs.
Free-Tier demo supports basic profanity/blocklist filtering.
"""

BLOCKLIST = {"badword1", "badword2"}

def filter_output(text: str) -> str:
    for bad in BLOCKLIST:
        text = text.replace(bad, "[REDACTED]")
    return text
