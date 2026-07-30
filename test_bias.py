from evaluator.toxicity import detect_toxicity

response = "You are a stupid idiot."

result = detect_toxicity(response)

print(result)