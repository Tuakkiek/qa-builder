import random
from collections import defaultdict


def split_dataset(
    qa_pairs: list[dict],
    train_ratio: float = 0.8,
    val_ratio: float = 0.1,
    test_ratio: float = 0.1,
    seed: int = 42,
) -> tuple[list[dict], list[dict], list[dict]]:

    total_ratio = train_ratio + val_ratio + test_ratio

    if abs(total_ratio - 1.0) > 1e-9:
        raise ValueError("Tổng train/val/test ratio phải bằng 1.0")

    chunks = defaultdict(list)

    for qa in qa_pairs:
        chunk_id = qa.get("chunk_id")

        if not chunk_id:
            raise ValueError("Q&A thiếu chunk_id")

        chunks[chunk_id].append(qa)

    chunk_ids = list(chunks.keys())

    random.seed(seed)
    random.shuffle(chunk_ids)

    total_chunks = len(chunk_ids)

    train_count = int(total_chunks * train_ratio)
    val_count = int(total_chunks * val_ratio)

    train_chunk_ids = chunk_ids[:train_count]

    val_chunk_ids = chunk_ids[
        train_count:train_count + val_count
    ]

    test_chunk_ids = chunk_ids[
        train_count + val_count:
    ]

    def collect(chunk_id_list):
        result = []

        for chunk_id in chunk_id_list:
            result.extend(chunks[chunk_id])

        return result

    train = collect(train_chunk_ids)
    val = collect(val_chunk_ids)
    test = collect(test_chunk_ids)

    return train, val, test


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


train, val, test = split_dataset(
    qa_pairs,
    seed=42
)

print("TRAIN")
for qa in train:
    print(qa)

print("\nVALIDATION")
for qa in val:
    print(qa)

print("\nTEST")
for qa in test:
    print(qa)