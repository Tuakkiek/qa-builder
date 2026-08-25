from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("all-MiniLM-L6-v2")


def remove_duplicate_questions(
    questions: list[str],
    threshold: float = 0.9
) -> list[str]:

    if not questions:
        return []

    embeddings = model.encode(questions)

    filtered_questions = []
    filtered_embeddings = []

    for i in range(len(questions)):
        is_duplicate = False

        for kept_embedding in filtered_embeddings:
            similarity = util.cos_sim(
                embeddings[i],
                kept_embedding
            ).item()

            if similarity > threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            filtered_questions.append(questions[i])
            filtered_embeddings.append(embeddings[i])

    return filtered_questions


questions = [
    "Machine Learning là gì?",
    "Machine Learning là cái gì?",
    "Python được sử dụng để làm gì?",
    "Python được dùng trong những lĩnh vực nào?",
    "Deep Learning khác Machine Learning như thế nào?"
]


result = remove_duplicate_questions(questions)


for question in result:
    print(question)