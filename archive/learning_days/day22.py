#import thư viện logging để ghi lại các hoạt động và lỗi của chương trình.
import logging
#import Path để xử lý đường dẫn thư mục.
from pathlib import Path 


#def hàm cài đặt và cấu hình bộ ghi log.
def setup_logger() -> logging.Logger: 
    #khai báo đường dẫn tới thư mục chứa file log.
    log_dir = Path("logs")
    #tạo thư mục nếu chưa có (exist_ok=True giúp ko báo lỗi nếu thư mục đã tồn tại).
    log_dir.mkdir(exist_ok=True)

    #khởi tạo object logger với tên định danh là "qa_builder".
    logger = logging.getLogger("qa_builder")
    #cài đặt mức độ ghi log tối thiểu là INFO (những log mức thấp hơn như DEBUG sẽ bị bỏ qua).
    logger.setLevel(logging.INFO)

    #nếu logger này đã được gắn handler (đã setup ở đâu đó rồi) -> trả về luôn để tránh bị in log trùng lặp 2-3 lần.
    if logger.handlers: 
        return logger

    #tạo cấu trúc định dạng cho dòng log: thời_gian - mức_độ_log - nội_dung_thông_báo.
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    #tạo handler để in log ra màn hình console (terminal).
    console_handler = logging.StreamHandler()
    #gắn cấu trúc định dạng vừa tạo cho console handler.
    console_handler.setFormatter(formatter)

    #tạo handler để lưu log xuống file "run.log" trong thư mục logs.
    file_handler = logging.FileHandler(
        log_dir / "run.log",
        #dùng utf-8 để ghi log tiếng Việt ko bị lỗi font.
        encoding="utf-8"
    )

    #gắn cấu trúc định dạng cho file handler.
    file_handler.setFormatter(formatter)

    #gắn console handler vào logger chính.
    logger.addHandler(console_handler)
    #gắn file handler vào logger chính.
    logger.addHandler(file_handler)

    #trả về logger đã cấu hình xong (lúc này nó vừa in ra màn hình vừa ghi vào file).
    return logger


#Code test tạo dữ liệu giả.
#gọi hàm khởi tạo logger.
logger = setup_logger() 

#ghi log thông báo thông tin bình thường.
logger.info("Bắt đầu chương trình")
#ghi log cảnh báo (chưa nghiêm trọng lắm nhưng cần chú ý).
logger.warning("File có dữ liệu thiếu")
#ghi log báo lỗi (nghiêm trọng).
logger.error("Không thể đọc file")