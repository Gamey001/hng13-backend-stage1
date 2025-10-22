# app/utils.py
import hashlib, json
from collections import Counter
from datetime import datetime, timezone

def sha256_of(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def compute_properties(value: str):
    cleaned = value.lower()
    return {
        "length": len(value),
        "is_palindrome": cleaned == cleaned[::-1],
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "sha256_hash": sha256_of(value),
        "character_frequency_map": dict(Counter(value))
    }

def iso_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def to_json(obj):
    return json.dumps(obj, ensure_ascii=False)

def from_json(text):
    import json
    return json.loads(text)
