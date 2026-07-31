import re

bias_words = [
    "women",
    "men",
    "male",
    "female",
    "emotional",
    "leadership",
    "leader",
    "muslim",
    "hindu",
    "christian",
    "black",
    "white",
    "poor",
    "rich"
]

stereotype_words = [
    "too emotional",
    "cannot",
    "can't",
    "always",
    "never",
    "inferior",
    "superior",
    "weak",
    "lazy",
    "violent"
]
negative_words = [
    "lazy",
    "stupid",
    "terrorist",
    "emotional",
    "weak",
    "inferior",
    "criminal",
    "dangerous",
    "useless"
]

def detect_bias(text):
    text = text.lower()

    # Split into complete words only
    words = re.findall(r"\b\w+\b", text)

    score = 0
    detected = []

    for word in bias_words:
        if word in words:
            detected.append(word)
            score += 10

    for word in stereotype_words:
        if word in words:
            detected.append(word)
            score += 20

    for word in negative_words:
        if word in words:
            detected.append(word)
            score += 25

    score = min(score, 100)

    if score >= 60:
        verdict = "High Bias"
    elif score >= 30:
        verdict = "Moderate Bias"
    else:
        verdict = "Low Bias"

    return {
        "bias_score": score,
        "keywords": detected,
        "verdict": verdict
    }