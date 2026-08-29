import logging

logging.basicConfig(
    filename="app.log",  # Tên file log sẽ tạo
    filemode="a",  # "a" = ghi tiếp vào cuối file, "w" = ghi đè
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S", # VD: 2026-08-29 14:49:53
    encoding="utf-8",  
)

logging.info("Ứng dụng được khởi chạy")
logging.error("Đã xảy ra lỗi khi tải dữ liệu")