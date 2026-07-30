from evaluator.scoring import calculate_safety_score

score = calculate_safety_score(
    bias=35,
    toxicity=20,
    accuracy=90
)

print(score)