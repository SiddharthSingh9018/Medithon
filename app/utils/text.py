import re

WORD_RE = re.compile(r"[a-zA-Z]{3,}")

def basic_tokens(text: str):
    return WORD_RE.findall(text.lower())
