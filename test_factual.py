from evaluator.factual import check_factual_accuracy

topic = "Isaac Newton"

response = "Isaac Newton discovered gravity."

result = check_factual_accuracy(topic, response)

print(result)