"""
Language identification filter for dataset.
Removes non-English examples.
"""

from langdetect import detect

def filter_lang(text: str, allowed_langs=("en",)):
    try:
        lang = detect(text)
        return lang in allowed_langs
    except:
        return False
