#import class SentenceTransformer và module util để xử lý vector ngữ nghĩa.
from sentence_transformers import SentenceTransformer, util


#khởi tạo model AI pre-trained có tên "all-MiniLM-L6-v2" (một model nhẹ, chạy nhanh chuyên dùng để tạo vector).
model = SentenceTransformer("all-MiniLM-L6-v2")


#tạo list chứa 3 câu mẫu để test độ tương đồng (câu 1 và 2 giống ý nhau, câu 3 khác chủ đề).
sentences = [
    "Machine Learning là gì?",
    "Machine Learning có nghĩa là gì?",
    "Python được sử dụng trong những lĩnh vực nào?"
]


#chuyển đổi (encode) các câu text dạng chữ thành các ma trận vector số (embeddings) để máy tính hiểu được.
embeddings = model.encode(sentences)


#in ra kích thước (shape) của ma trận vector kết quả (thường là tổng số câu x số chiều của vector).
print("Shape:", embeddings.shape)
#in dòng trống cho dễ nhìn.
print()


#tính độ tương đồng cosine (cosine similarity) giữa vector của câu 1 (index 0) và câu 2 (index 1).
#dùng hàm .item() để rút lấy một giá trị số thực (float) duy nhất từ tensor kết quả trả về.
similarity_1_2 = util.cos_sim(
    embeddings[0],
    embeddings[1]
).item()

#tính độ tương đồng giữa câu 1 (index 0) và câu 3 (index 2).
similarity_1_3 = util.cos_sim(
    embeddings[0],
    embeddings[2]
).item()

#tính độ tương đồng giữa câu 2 (index 1) và câu 3 (index 2).
similarity_2_3 = util.cos_sim(
    embeddings[1],
    embeddings[2]
).item()


#in ra màn hình kết quả so sánh độ giống nhau giữa câu 1 và câu 2.
print("Câu 1:", sentences[0])
print("Câu 2:", sentences[1])
print("Similarity:", similarity_1_2)

print()

#in kết quả so sánh giữa câu 1 và câu 3.
print("Câu 1:", sentences[0])
print("Câu 3:", sentences[2])
print("Similarity:", similarity_1_3)

print()

#in kết quả so sánh giữa câu 2 và câu 3.
print("Câu 2:", sentences[1])
print("Câu 3:", sentences[2])
print("Similarity:", similarity_2_3)