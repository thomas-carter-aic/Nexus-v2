"""
Safety helpers
"""

BLOCKLIST = {"badword1", "badword2"}

def filter_output(text: str) -> str:
    for bad in BLOCKLIST:
        text = text.replace(bad, "[REDACTED]")
    return text
