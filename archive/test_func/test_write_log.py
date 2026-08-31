#import thư viện logging chuẩn.
import logging

#cấu hình ghi log trực tiếp ra file.
logging.basicConfig(
    #tên file log sẽ tạo.
    filename="app.log",  
    #chế độ ghi: "a" là ghi nối tiếp vào cuối file (append), "w" là ghi đè.
    filemode="a",  
    #mức độ log tối thiểu là DEBUG.
    level=logging.DEBUG,
    #định dạng dòng log: thời gian - cấp độ - nội dung.
    format="%(asctime)s - %(levelname)s - %(message)s", 
    #định dạng hiển thị ngày giờ (ví dụ: 2026-08-29 14:49:53).
    datefmt="%Y-%m-%d %H:%M:%S", 
    #bảng mã UTF-8 để ghi tiếng Việt không bị lỗi font.
    encoding="utf-8",  
)

#ghi log thông tin khởi chạy ứng dụng.
logging.info("Ứng dụng được khởi chạy")
#ghi log báo lỗi tải dữ liệu.
logging.error("Đã xảy ra lỗi khi tải dữ liệu")