import re

toxic_words = [
    "weak",
    "idiot",
    "stupid",
    "hate",
    "kill",
    "female",
    "lower",
    "ugly",
    "fool",
    "moron",
    "dumb",
    "loser"
]

def detect_toxicity(text):
    text = text.lower()

    words = re.findall(r"\b\w+\b", text)

    scoring = 0
    detected = []

    for word in toxic_words:
        if word in words:
            detected.append(word)
            scoring += 20

    scoring = min(scoring, 100)

    if scoring >= 60:
        verdict = "Highly Toxic"
    elif scoring >= 30:
        verdict = "Moderately Toxic"
    else:
        verdict = "Low Toxicity"

    return {
        "toxicity_score": scoring,
        "detected_words": detected,
        "verdict": verdict
    }