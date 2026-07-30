import re

toxic_words = [
    "idiot",
    "stupid",
    "hate",
    "kill",
    "terrorist",
    "ugly",
    "fool",
    "moron",
    "dumb",
    "loser"
]

def detect_toxicity(text):
    text = text.lower()

    words = re.findall(r"\b\w+\b", text)

    score = 0
    detected = []

    for word in toxic_words:
        if word in words:
            detected.append(word)
            score += 20

    score = min(score, 100)

    if score >= 60:
        verdict = "Highly Toxic"
    elif score >= 30:
        verdict = "Moderately Toxic"
    else:
        verdict = "Low Toxicity"

    return {
        "toxicity_score": score,
        "detected_words": detected,
        "verdict": verdict
    }