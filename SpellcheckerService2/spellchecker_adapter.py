import re

from spellchecker import SpellChecker

SPELLCHECKER_INSTANCE = SpellChecker()


def predict_misspelling(text: str) -> dict:
    tokens = list(filter(None, re.split(r"[\s.,!?:;-]+", text)))
    unique_tokens = set(tokens)
    candidates_list = [(SPELLCHECKER_INSTANCE.candidates(token), token) for token in tokens]
    misspelled = set()
    corrected_content = text.lower()

    for candidates, token in candidates_list:
        if candidates is not None and token not in candidates:
            misspelled.add(token)
            corrected_content = corrected_content.replace(token, candidates.pop())

    return {"misspelled_tokens": misspelled,
            "corrected_content": corrected_content,
            "misspelled_rate": (len(misspelled) / len(unique_tokens)) if len(
                unique_tokens) != 0 else 0,
            "misspelled_token_count": len(misspelled)}
