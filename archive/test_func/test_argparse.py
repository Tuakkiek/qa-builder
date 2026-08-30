import argparse

parser = argparse.ArgumentParser() 

parser.add_argument(
    "--input-dir", 
    required=True,
    help="Thư mục chứa file md"
)

parser.add_argument(
    "--output-dir",
    required=True,
    help="Thư mục lưu kết quả"
)

args = parser.parse_args() 

print("Input dir: " + args.input_dir)
print("Output dir: " + args.output_dir)

