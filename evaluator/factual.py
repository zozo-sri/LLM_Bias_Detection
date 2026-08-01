import wikipediaapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

#Loading the embedding model 
model = SentenceTransformer("all-MiniLM-L6-v2")

wikiped = wikipediaapi.Wikipedia(
    language='en',
    user_agent='LLM-Bias-Detection/1.0 (student project)'
)


def check_factual_accuracy(topic, response):
    page = wikiped.page(topic)

    if not page.exists():
        return {
            "accuracy_score": 0,
            "reference": "Wikipedia page not found."
        }

    reference = page.summary[:500]

    embeddings = model.encode([response, reference])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    accuracy = round(similarity * 100, 2)

    return {
        "accuracy_score": accuracy,
        "reference": reference
    }