import streamlit as st
import pandas as pd
from difflib import SequenceMatcher

from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def phrase_exists(phrase, text, threshold=0.65):
    """
    Checks if a domain phrase exists in text using:
    1. Direct substring
    2. Sliding window fuzzy match
    """
    phrase = phrase.lower().strip()
    text = text.lower()

    if phrase in text:
        return True

    phrase_len = len(phrase.split())
    words = text.split()

    for i in range(len(words) - phrase_len + 1):
        window = " ".join(words[i:i + phrase_len])
        if similarity(phrase, window) >= threshold:
            return True

    return False
