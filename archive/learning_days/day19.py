#import thư viện random để xáo trộn danh sách.
import random
#import defaultdict để gom nhóm dữ liệu nhanh mà ko bị lỗi key.
from collections import defaultdict


#def hàm chia dữ liệu thành 3 tập train, val, test dựa trên tỷ lệ.
def split_dataset(
    qa_pairs: list[dict],
    train_ratio: float = 0.8, #80% cho huấn luyện.
    val_ratio: float = 0.1,   #10% cho kiểm định.
    test_ratio: float = 0.1,  #10% cho kiểm tra.
    seed: int = 42,           #cố định random để kết quả ko đổi giữa các lần chạy.
) -> tuple[list[dict], list[dict], list[dict]]:

    #tính tổng tỷ lệ.
    total_ratio = train_ratio + val_ratio + test_ratio

    #kiểm tra tổng tỷ lệ có = 1 ko (dùng sai số 1e-9 để tránh lỗi làm tròn số thực của python).
    if abs(total_ratio - 1.0) > 1e-9:
        #nếu khác 1 -> báo lỗi.
        raise ValueError("Tổng train/val/test ratio phải bằng 1.0")

    #tạo dict mặc định là list để nhóm các q&a theo chunk_id.
    chunks = defaultdict(list)

    #duyệt qua từng cặp q&a.
    for qa in qa_pairs:
        #lấy chunk_id của cặp q&a hiện tại.
        chunk_id = qa.get("chunk_id")

        #nếu thiếu chunk_id -> báo lỗi vì ko thể nhóm.
        if not chunk_id:
            raise ValueError("Q&A thiếu chunk_id")

        #thêm q&a vào nhóm chunk_id tương ứng (giúp các q&a cùng 1 đoạn text ko bị xé lẻ ra 2 tập khác nhau).
        chunks[chunk_id].append(qa)

    #lấy danh sách tất cả các chunk_id hiện có.
    chunk_ids = list(chunks.keys())

    #cố định random seed.
    random.seed(seed)
    #xáo trộn ngẫu nhiên danh sách chunk_id.
    random.shuffle(chunk_ids)

    #đếm tổng số chunk_id.
    total_chunks = len(chunk_ids)

    #tính toán số lượng chunk cho từng tập train, val (ép kiểu int để bỏ phần thập phân).
    train_count = int(total_chunks * train_ratio)
    val_count = int(total_chunks * val_ratio)

    #cắt lấy danh sách chunk_id cho tập train (từ đầu đến vị trí train_count).
    train_chunk_ids = chunk_ids[:train_count]

    #cắt lấy chunk_id cho tập val (tiếp nối ngay sau tập train).
    val_chunk_ids = chunk_ids[
        train_count:train_count + val_count
    ]

    #phần chunk_id còn lại ở cuối dành cho tập test.
    test_chunk_ids = chunk_ids[
        train_count + val_count:
    ]

    #def hàm con dùng để gom các q&a từ danh sách chunk_id đã bị cắt.
    def collect(chunk_id_list):
        #tạo list rỗng chứa kết quả.
        result = []

        #duyệt qua từng chunk_id trong danh sách truyền vào.
        for chunk_id in chunk_id_list:
            #đưa tất cả q&a thuộc chunk_id đó vào list kết quả.
            result.extend(chunks[chunk_id])

        #trả về list các cặp q&a.
        return result

    #gọi hàm collect để lấy dữ liệu thực tế cho tập train.
    train = collect(train_chunk_ids)
    #lấy dữ liệu tập val.
    val = collect(val_chunk_ids)
    #lấy dữ liệu tập test.
    test = collect(test_chunk_ids)

    #trả về 3 tập dữ liệu đã chia xong.
    return train, val, test


#Code test tạo dữ liệu giả.
#tạo list mẫu chứa các cặp q&a, lưu ý là có nhiều q&a dùng chung 1 chunk_id.
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


#gọi hàm chia dữ liệu thành 3 tập.
train, val, test = split_dataset(
    qa_pairs,
    seed=42
)

#in danh sách q&a thuộc tập train.
print("TRAIN")
for qa in train:
    print(qa)

#in danh sách q&a thuộc tập val.
print("\nVALIDATION")
for qa in val:
    print(qa)

#in danh sách q&a thuộc tập test.
print("\nTEST")
for qa in test:
    print(qa)