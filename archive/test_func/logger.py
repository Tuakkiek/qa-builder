#import thư viện logging chuẩn của Python để ghi nhật ký hoạt động.
import logging 
#import Path để thao tác đường dẫn thư mục log.
from pathlib import Path 

#def hàm cấu hình hệ thống ghi log (Logger) xuất ra cả terminal lẫn file log.
def setup_logger() -> logging.Logger: 
    #khởi tạo đường dẫn thư mục logs.
    log_dir = Path("logs")
    #tạo thư mục nếu chưa có.
    log_dir.mkdir(exist_ok=True)

    #lấy hoặc tạo logger có tên định danh "qa_builder".
    logger = logging.getLogger("qa_builder")
    #thiết lập mức độ log tối thiểu là INFO.
    logger.setLevel(logging.INFO)

    #kiểm tra nếu logger đã có handler rồi thì return luôn để tránh bị duplicate log.
    # if logger.handlers:
    #     return logger

    #định dạng mẫu hiển thị log: thời gian - mức độ - nội dung tin nhắn.
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    #tạo handler để in log ra màn hình console / terminal.
    console_handler = logging.StreamHandler() 
    console_handler.setFormatter(formatter)

    #tạo handler để ghi log vào file run.log với bảng mã UTF-8.
    file_handler = logging.FileHandler(
        log_dir / "run.log", 
        encoding = "utf-8"
    )
    file_handler.setFormatter(formatter)

    #gắn các handler vào logger.
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    #trả về đối tượng logger đã cấu hình xong.
    return logger

#thử nghiệm gọi hàm cấu hình logger.
logger = setup_logger()
logger = setup_logger()
logger = setup_logger()
logger = setup_logger()
logger = setup_logger()

#ghi log ở các mức độ khác nhau.
logger.info("Bắt đầu chương trình")
logger.warning("File có dữ liệu thiếu")
logger.error("Không thể đọc file")
