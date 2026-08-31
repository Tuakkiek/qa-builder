#import thư viện random để xáo trộn dữ liệu ngẫu nhiên.
import random
#import defaultdict từ collections để nhóm các câu hỏi theo chunk_id.
from collections import defaultdict


#def hàm chia tập dữ liệu Q&A thành 3 tập train, validation và test theo tỷ lệ và nhóm chunk.
def split_dataset(
    qa_pairs: list[dict],
    #tỷ lệ mặc định cho tập train là 80%.
    train_ratio: float = 0.8,
    #tỷ lệ mặc định cho tập val là 10%.
    val_ratio: float = 0.1,
    #tỷ lệ mặc định cho tập test là 10%.
    test_ratio: float = 0.1,
    #seed ngẫu nhiên cố định để kết quả chia có thể tái lập.
    seed: int = 42,
) -> tuple[list[dict], list[dict], list[dict]]:

    #tính tổng tỷ lệ.
    total_ratio = train_ratio + val_ratio + test_ratio

    #kiểm tra tổng 3 tỷ lệ có xấp xỉ bằng 1.0 hay không (dùng sai số 1e-9 để tránh lỗi số thực).
    if abs(total_ratio - 1.0) > 1e-9:
        raise ValueError("Tổng train/val/test ratio phải bằng 1.0")

    #gom các câu hỏi Q&A vào từng nhóm tương ứng với chunk_id để tránh data leakage.
    chunks = defaultdict(list)

    #duyệt qua từng cặp Q&A.
    for qa in qa_pairs:
        chunk_id = qa.get("chunk_id")

        #nếu câu hỏi không có chunk_id -> báo lỗi.
        if not chunk_id:
            raise ValueError("Q&A thiếu chunk_id")

        #thêm cặp Q&A vào nhóm chunk_id tương ứng.
        chunks[chunk_id].append(qa)

    #lấy danh sách các chunk_id duy nhất.
    chunk_ids = list(chunks.keys())

    #thiết lập seed ngẫu nhiên và xáo trộn danh sách chunk_id.
    random.seed(seed)
    random.shuffle(chunk_ids)

    #tính tổng số lượng chunk.
    total_chunks = len(chunk_ids)

    #tính số lượng chunk cho tập train và val.
    train_count = int(total_chunks * train_ratio)
    val_count = int(total_chunks * val_ratio)

    #cắt danh sách chunk_id cho tập train.
    train_chunk_ids = chunk_ids[:train_count]

    #cắt danh sách chunk_id cho tập validation.
    val_chunk_ids = chunk_ids[
        train_count:train_count + val_count
    ]

    #cắt danh sách chunk_id cho tập test (phần còn lại).
    test_chunk_ids = chunk_ids[
        train_count + val_count:
    ]

    #hàm phụ để gom tất cả các cặp Q&A từ danh sách chunk_id.
    def collect(chunk_id_list):
        result = []

        for chunk_id in chunk_id_list:
            result.extend(chunks[chunk_id])

        return result

    #gom các Q&A tương ứng cho từng tập.
    train = collect(train_chunk_ids)
    val = collect(val_chunk_ids)
    test = collect(test_chunk_ids)

    #trả về bộ 3 tập dữ liệu (train, val, test).
    return train, val, test


#dữ liệu mẫu 14 cặp Q&A thuộc 10 chunk khác nhau.
qa_pairs = [
    {
        "question": "Q1",
        "answer": "A1",
        "chunk_id": "chunk_001"
    },
    {
        "question": "Q2",
        "answer": "A2",
        "chunk_id": "chunk_001"
    },
    {
        "question": "Q3",
        "answer": "A3",
        "chunk_id": "chunk_002"
    },
    {
        "question": "Q4",
        "answer": "A4",
        "chunk_id": "chunk_002"
    },
    {
        "question": "Q5",
        "answer": "A5",
        "chunk_id": "chunk_003"
    },
    {
        "question": "Q6",
        "answer": "A6",
        "chunk_id": "chunk_004"
    },
    {
        "question": "Q7",
        "answer": "A7",
        "chunk_id": "chunk_004"
    },
    {
        "question": "Q8",
        "answer": "A8",
        "chunk_id": "chunk_005"
    },
    {
        "question": "Q9",
        "answer": "A9",
        "chunk_id": "chunk_006"
    },
    {
        "question": "Q10",
        "answer": "A10",
        "chunk_id": "chunk_007"
    },
    {
        "question": "Q11",
        "answer": "A11",
        "chunk_id": "chunk_007"
    },
    {
        "question": "Q12",
        "answer": "A12",
        "chunk_id": "chunk_008"
    },
        {
        "question": "Q13",
        "answer": "A13",
        "chunk_id": "chunk_009"
    },
        {
        "question": "Q14",
        "answer": "A14",
        "chunk_id": "chunk_010"
    },
]


#gọi hàm chia tập dữ liệu.
train, val, test = split_dataset(
    qa_pairs,
    seed=42
)

#in ra các phần tử của tập TRAIN.
print("TRAIN")
for qa in train:
    print(qa)

#in ra các phần tử của tập VALIDATION.
print("\nVALIDATION")
for qa in val:
    print(qa)

#in ra các phần tử của tập TEST.
print("\nTEST")
for qa in test:
    print(qa)