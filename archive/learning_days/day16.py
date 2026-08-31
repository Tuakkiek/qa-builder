#def hàm lọc các cặp q&a dựa trên số từ tối thiểu của câu hỏi.
def filter_qa(
    qa_pairs: list[dict], 
    min_words: int = 5 #giới hạn mặc định câu hỏi phải có ít nhất 5 từ.
) -> list[dict]: 

    #tạo list rỗng để chứa các cặp q&a đạt chuẩn sau khi lọc.
    filtered = [] 

    #duyệt qua từng cặp q&a trong danh sách truyền vào.
    for qa in qa_pairs: 

        #lấy nội dung câu hỏi an toàn (nếu ko có key thì trả về chuỗi rỗng) và xóa khoảng trắng dư 2 lề.
        question = qa.get("question", "").strip()

        #tách câu hỏi thành mảng các từ rồi đếm số lượng.
        word_count = len(question.split())

        #nếu độ dài câu hỏi ngắn hơn mức quy định.
        if word_count < min_words: 
            #bỏ qua luôn, sang cặp q&a tiếp theo.
            continue 
        
        #nếu đủ số từ -> thêm cặp q&a này vào list kết quả.
        filtered.append(qa)
    
    #trả về danh sách các cặp q&a đã được lọc.
    return filtered


#Code test tạo dữ liệu giả.
#tạo list mẫu chứa các cặp q&a.
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

#gọi hàm lọc, dùng mức mặc định là 5 từ (những câu hỏi < 5 từ sẽ bị loại bỏ).
result = filter_qa(qa_pairs)


#duyệt qua list kết quả và in ra màn hình.
for qa in result:
    #in nội dung câu hỏi.
    print("Question:", qa["question"])
    #in nội dung câu trả lời.
    print("Answer:", qa["answer"])