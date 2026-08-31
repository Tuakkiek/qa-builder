#import thư viện argparse để đọc tham số truyền vào từ dòng lệnh (CLI).
import argparse

#khởi tạo parser để định nghĩa các đối số.
parser = argparse.ArgumentParser() 

#thêm tham số bắt buộc --input-dir: đường dẫn thư mục đầu vào.
parser.add_argument(
    "--input-dir", 
    required=True,
    help="Thư mục chứa file md"
)

#thêm tham số bắt buộc --output-dir: đường dẫn thư mục đầu ra.
parser.add_argument(
    "--output-dir",
    required=True,
    help="Thư mục lưu kết quả"
)

#phân tích các tham số truyền vào từ dòng lệnh.
args = parser.parse_args() 

#in các giá trị tham số nhận được ra màn hình.
print("Input dir: " + args.input_dir)
print("Output dir: " + args.output_dir)

