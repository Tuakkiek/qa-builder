#import Path và json để xử lý file và dữ liệu json.
from pathlib import Path
import json

#khai báo đường dẫn lưu file json đếm request.
REQUEST_COUNT_FILE = Path("logs/request_count.json")

#def hàm lưu tổng số lượt request vào file json.
def save_request_count(count: int) -> None:
    #tạo thư mục cha (logs/) nếu chưa tồn tại (exist_ok=True tránh lỗi nếu đã có).
    REQUEST_COUNT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    #mở file ở chế độ ghi ("w") với mã hoá utf-8.
    with open(
        REQUEST_COUNT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        #ghi dữ liệu dict vào file json với định dạng thụt lề 4 space (indent=4).
        json.dump(
            {"request_count": count},
            file,
            ensure_ascii=False,
            indent=4
        )

