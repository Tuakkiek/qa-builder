#import class và module xử lý vector từ thư viện sentence_transformers.
from sentence_transformers import SentenceTransformer, util


#khởi tạo model AI pre-trained để chuyển đổi văn bản thành vector ngữ nghĩa.
model = SentenceTransformer("all-MiniLM-L6-v2")


#def hàm loại bỏ các câu hỏi trùng lặp ý nghĩa.
def remove_duplicate_questions(
    questions: list[str],
    threshold: float = 0.9 #ngưỡng độ tương đồng mặc định là 0.9 (giống nhau >= 90% thì coi là trùng).
) -> list[str]:

    #nếu list câu hỏi rỗng -> trả về list rỗng luôn.
    if not questions:
        return []

    #mã hóa (encode) tất cả câu hỏi đầu vào thành một tập hợp các vector số.
    embeddings = model.encode(questions)

    #tạo list rỗng chứa các câu hỏi đã được lọc (ko bị trùng).
    filtered_questions = []
    #tạo list rỗng chứa vector tương ứng của các câu hỏi đã được lọc.
    filtered_embeddings = []

    #duyệt qua từng câu hỏi dựa vào vị trí index (i).
    for i in range(len(questions)):
        #tạo cờ (flag) đánh dấu, mặc định là False (chưa bị trùng).
        is_duplicate = False

        #duyệt qua các vector của những câu hỏi ĐÃ ĐƯỢC GIỮ LẠI trước đó.
        for kept_embedding in filtered_embeddings:
            #tính độ tương đồng cosine giữa câu đang xét và câu đã được giữ.
            similarity = util.cos_sim(
                embeddings[i],
                kept_embedding
            ).item()

            #nếu độ giống nhau vượt qua ngưỡng cho phép -> xác định là câu trùng ý.
            if similarity > threshold:
                #bật cờ trùng lặp lên True.
                is_duplicate = True
                #thoát khỏi vòng lặp so sánh ngay lập tức (ko cần so với các câu khác nữa).
                break

        #nếu câu hỏi đang xét ko bị trùng (cờ vẫn là False).
        if not is_duplicate:
            #thêm câu hỏi đó vào list kết quả.
            filtered_questions.append(questions[i])
            #thêm luôn vector của nó vào list vector giữ lại để làm gốc so sánh cho các vòng lặp sau.
            filtered_embeddings.append(embeddings[i])

    #trả về danh sách các câu hỏi đã lọc sạch trùng lặp.
    return filtered_questions


#Code test tạo dữ liệu giả.
#tạo list chứa các câu hỏi (trong đó có vài câu dùng từ khác nhưng giống ý nhau).
questions = [
    "Machine Learning là gì?",
    "Machine Learning là cái gì?",
    "Python được sử dụng để làm gì?",
    "Python được dùng trong những lĩnh vực nào?",
    "Deep Learning khác Machine Learning như thế nào?"
]


#gọi hàm lọc, những câu giống ý (>= 90%) sẽ bị vứt bỏ, chỉ giữ lại câu xuất hiện trước.
result = remove_duplicate_questions(questions)


#duyệt qua list kết quả và in ra màn hình.
for question in result:
    print(question)