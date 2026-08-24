def filter_qa(
    qa_pairs: list[dict], 
    min_words: int = 5
) -> list[dict]: 

    filtered = [] 

    for qa in qa_pairs: 

        question = qa.get("question", "").strip()

        word_count = len(question.split())

        if word_count < min_words: 
            continue 
        
        filtered.append(qa)
    
    return filtered

qa_pairs = [
    {
        "question": "AI là gì?",
        "answer": "AI là trí tuệ nhân tạo."
    },
    {
        "question": "Machine Learning hoạt động như thế nào?",
        "answer": "Machine Learning cho phép máy học từ dữ liệu."
    },
    {
        "question": "Deep Learning khác Machine Learning truyền thống ở điểm nào?",
        "answer": "Deep Learning sử dụng mạng neural nhiều tầng."
    }
]

result = filter_qa(qa_pairs)

for qa in result:
    print("Question:", qa["question"])
    print("Answer:", qa["answer"])