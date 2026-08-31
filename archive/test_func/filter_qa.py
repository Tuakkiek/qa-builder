#def hàm lọc danh sách các cặp Q&A, loại bỏ các câu hỏi quá ngắn (dưới min_words từ).
def filter_qa(
    qa_pairs: list[dict],
    #giới hạn mặc định tối thiểu 5 từ cho câu hỏi.
    min_words: int = 5
) -> list[dict]: 

    #tạo list rỗng chứa các cặp Q&A đạt chuẩn.
    filtered = [] 

    #duyệt qua từng cặp Q&A trong danh sách.
    for qa in qa_pairs: 

        #lấy nội dung câu hỏi.
        question = qa["question"]

        #nếu số từ của câu hỏi nhỏ hơn ngưỡng quy định -> bỏ qua (không lấy).
        if len(question.split()) < min_words: 
            continue
        
        #nếu hợp lệ -> thêm cặp Q&A vào danh sách kết quả.
        filtered.append(qa)

    #trả về danh sách Q&A đã lọc.
    return filtered

#danh sách các cặp Q&A mẫu kiểm tra.
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

#gọi hàm lọc Q&A.
result = filter_qa(qa_pairs)

#in ra các cặp Q&A sau khi lọc ("AI là gì?" sẽ bị loại vì chỉ có 3 từ).
for qa in result: 
    print("Question: ", qa["question"])
    print("Answer: ", qa["answer"])