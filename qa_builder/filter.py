import re
from functools import lru_cache

# Danh sách các từ phủ định thường gặp trong tiếng Việt và tiếng Anh
NEGATION_WORDS = {
    "không", "chưa", "chẳng", "không phải", "khum", "ko",
    "not", "never", "no", "neither", "nor", "none"
}

#Kiểm tra độ dài câu hỏi
def is_question_long_enough(question: str, min_words: int = 5) -> bool:
    return len(question.split()) >= min_words

#Kiểm tra xem câu có chứa yếu tố phủ định hay không.
def extract_negation(text: str) -> bool:
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    return any(word in NEGATION_WORDS for word in words)

#Rule Check
#Trả về True nếu 1 câu Khẳng định còn câu kia là Phủ định (ngược nghĩa).
def has_negation_conflict(text1: str, text2: str) -> bool:
    neg1 = extract_negation(text1)
    neg2 = extract_negation(text2)
    return neg1 != neg2  # Lệch nhau tính phủ định -> có xung đột


@lru_cache(maxsize=1)
def load_embedding_model(): 
    from sentence_transformers import SentenceTransformer
    # return SentenceTransformer("all-MiniLM-L6-v2")
    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")




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
    filtered_questions = []


    for i, qa in enumerate(qa_pairs):
        is_duplicate = False

        #Vòng lặp so sánh câu hiện tại với các câu đã giữ lại
        for j, kept_embedding in enumerate(filtered_embeddings):
            #1. Kiểm tra độ tương đồng ngữ nghĩa bằng Embedding
            similarity = util.cos_sim(
                embeddings[i],
                kept_embedding,
            ).item()

            # Nếu độ tương đồng cao (> threshold)
            if similarity > threshold:
                #2. Kiểm tra luật Phủ định (Rule Check)
                #Nếu bị ngược nghĩa -> KO coi là trung lặp -> giữa lại
                if has_negation_conflict(questions[i], filtered_questions[j]):
                    continue  # Bỏ qua, ko đánh dấu là trùng
                
                #Nếu ko bị ngược nghĩa -> coi là trùng -> loại bỏ
                is_duplicate = True
                break

        if not is_duplicate:
            filtered.append(qa)
            filtered_embeddings.append(embeddings[i])
            filtered_questions.append(questions[i])

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

