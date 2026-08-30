import json
import random
from collections import defaultdict
from pathlib import Path


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

    if total_chunks == 0:
        return [], [], []

    train_count = int(total_chunks * train_ratio)
    val_count = int(total_chunks * val_ratio)

    if train_count == 0:
        train_count = 1

    train_chunk_ids = chunk_ids[:train_count]
    val_chunk_ids = chunk_ids[train_count:train_count + val_count]
    test_chunk_ids = chunk_ids[train_count + val_count:]

    def collect(chunk_id_list: list[str]) -> list[dict]:
        result = []

        for chunk_id in chunk_id_list:
            result.extend(chunks[chunk_id])

        return result

    train = collect(train_chunk_ids)
    val = collect(val_chunk_ids)
    test = collect(test_chunk_ids)

    return train, val, test


def to_alpaca_format(qa_pairs: list[dict]) -> list[dict]:
    records = []

    for qa in qa_pairs:
        record = {
            "instruction": qa["question"],
            "input": "",
            "output": qa["answer"],
        }

        if "chunk_id" in qa:
            record["chunk_id"] = qa["chunk_id"]

        if "source_file" in qa:
            record["source_file"] = qa["source_file"]

        records.append(record)

    return records


def write_jsonl(data: list[dict], filepath: str | Path) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        for item in data:
            line = json.dumps(item, ensure_ascii=False)
            file.write(line + "\n")
