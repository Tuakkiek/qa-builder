import argparse
from pathlib import Path

from qa_builder import (
    chunk_text,
    extract_md,
    filter_qa,
    generate_qa,
    setup_logger,
    split_dataset,
    to_alpaca_format,
    write_jsonl,
)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-dir",
        required=True,
        help="Thư mục chứa file .md",
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        help="Thư mục chứa kết quả",
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=300,
        help="Số từ tối đa trong mỗi chunk",
    )

    parser.add_argument(
        "--questions-per-chunk",
        type=int,
        default=3,
        help="Số Q&A cần sinh cho mỗi chunk",
    )

    parser.add_argument(
        "--limit-files",
        type=int,
        default=None,
        help="Giới hạn số file để học và test nhanh",
    )

    parser.add_argument(
        "--limit-chunks",
        type=int,
        default=None,
        help="Giới hạn số chunk để tránh gọi API quá nhiều",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = setup_logger()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        raise FileNotFoundError(f"Không tìm thấy thư mục input: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    md_files = sorted(
        input_dir.glob("*.md"),
        key=lambda path: (path.name != "sample.md", path.name.lower()),
    )

    if args.limit_files is not None:
        md_files = md_files[:args.limit_files]

    logger.info("Tìm thấy %s file markdown", len(md_files))

    all_chunks = []

    for md_file in md_files:
        logger.info("Đang trích xuất %s", md_file.name)
        units = extract_md(md_file)
        chunks = chunk_text(units, chunk_size=args.chunk_size)
        all_chunks.extend(chunks)
        logger.info("Đã tạo %s chunk từ %s", len(chunks), md_file.name)

    if args.limit_chunks is not None:
        all_chunks = all_chunks[:args.limit_chunks]

    logger.info("Tổng số chunk: %s", len(all_chunks))

    qa_pairs = []

    for index, chunk in enumerate(all_chunks, start=1):
        logger.info(
            "Đang sinh Q&A cho chunk %s/%s: %s",
            index,
            len(all_chunks),
            chunk.chunk_id,
        )

        chunk_qa_pairs = generate_qa(
            chunk,
            num_questions=args.questions_per_chunk,
        )

        if not chunk_qa_pairs:
            logger.error("API key lỗi hoặc hết quota. Dừng chương trình.")
            break

        qa_pairs.extend(chunk_qa_pairs)

        write_jsonl(
            to_alpaca_format(qa_pairs),
            output_dir / "qa_dataset.jsonl",
        )

        logger.info(
            "Đã lưu %s Q&A",
            len(qa_pairs),
        )

    logger.info("Đã sinh %s cặp Q&A", len(qa_pairs))

    qa_pairs = filter_qa(qa_pairs)
    logger.info("Giữ lại %s cặp Q&A sau khi lọc", len(qa_pairs))

    train, val, test = split_dataset(qa_pairs)

    write_jsonl(to_alpaca_format(qa_pairs), output_dir / "qa_dataset.jsonl")
    write_jsonl(to_alpaca_format(train), output_dir / "train.jsonl")
    write_jsonl(to_alpaca_format(val), output_dir / "val.jsonl")
    write_jsonl(to_alpaca_format(test), output_dir / "test.jsonl")

    logger.info("Hoàn tất. Kết quả đã được ghi vào %s", output_dir)


if __name__ == "__main__":
    main()
