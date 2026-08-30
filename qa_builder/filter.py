from functools import lru_cache


def is_question_long_enough(question: str, min_words: int = 5) -> bool:
    return len(question.split()) >= min_words


@lru_cache(maxsize=1)
def load_embedding_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


def remove_duplicate_qa(
    qa_pairs: list[dict],
    threshold: float = 0.9,
) -> list[dict]:
    if not qa_pairs:
        return []

    from sentence_transformers import util

    questions = [qa["question"] for qa in qa_pairs]
    model = load_embedding_model()
    embeddings = model.encode(questions)

    filtered = []
    filtered_embeddings = []

    for i, qa in enumerate(qa_pairs):
        is_duplicate = False

        for kept_embedding in filtered_embeddings:
            similarity = util.cos_sim(
                embeddings[i],
                kept_embedding,
            ).item()

            if similarity > threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            filtered.append(qa)
            filtered_embeddings.append(embeddings[i])

    return filtered


def filter_qa(
    qa_pairs: list[dict],
    min_words: int = 5,
    remove_duplicates: bool = True,
    duplicate_threshold: float = 0.9,
) -> list[dict]:
    filtered = []

    for qa in qa_pairs:
        question = qa.get("question", "")
        answer = qa.get("answer", "")

        if not question or not answer:
            continue

        if not is_question_long_enough(question, min_words=min_words):
            continue

        filtered.append(qa)

    if remove_duplicates:
        filtered = remove_duplicate_qa(
            filtered,
            threshold=duplicate_threshold,
        )

    return filtered

