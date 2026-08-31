#import Path để thao tác với đường dẫn file hệ thống.
from pathlib import Path
#import thư viện json để đọc định dạng json.
import json

#khai báo đường dẫn đến file lưu số lượng request đã gửi.
REQUEST_COUNT_FILE = Path("logs/request_count.json")

#def hàm đọc tổng số request đã lưu từ file log.
def load_request_count() -> int: 
    #nếu file chưa tồn tại -> trả về 0.
    if not REQUEST_COUNT_FILE.exists(): 
        return 0 
    
    #mở file ở chế độ đọc với chuẩn mã hoá UTF-8.
    with open(
        REQUEST_COUNT_FILE, 
        "r", 
        encoding = "utf-8"
    ) as file: 
        #đọc dữ liệu file và chuyển thành dictionary.
        data = json.load(file) 
    
    #lấy giá trị của key "request_count", nếu không có key này thì trả về mặc định là 0.
    return data.get("request_count", 0)

#in ra tổng số request đã load được.
print(load_request_count())

