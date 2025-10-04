"""
Simple PII scrubber for training data.
Removes emails, phone numbers, and SSNs (basic regex).
"""

import re

EMAIL_RE = re.compile(r'\S+@\S+')
PHONE_RE = re.compile(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b')
SSN_RE = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

def scrub_pii(text: str):
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    text = SSN_RE.sub("[SSN]", text)
    return text
