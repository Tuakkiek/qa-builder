import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser() 

    parser.add_argument(
        "--input-dir", 
        required=True,
        help="Thư mục chứa file md"
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        help="Thư mục chứa kết quả"
    )

    args = parser.parse_args() 

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        raise FileNotFoundError(
            f"Input directory not found: {input_dir}"
        )
        
    output_dir.mkdir(
        parents = True, 
        exist_ok = True
    )

    md_files = list(
        input_dir.glob("*.md")
    )

    for file in md_files: 
        print(file)

if __name__ == "__main__":
    main() 