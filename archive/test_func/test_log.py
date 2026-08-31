#import thư viện logging chuẩn.
import logging

#cấu hình cơ bản mức log tối thiểu là INFO (các log DEBUG sẽ bị ẩn đi).
logging.basicConfig(level=logging.INFO)

#thử nghiệm ghi log ở các cấp độ nghiêm trọng tăng dần.
logging.debug("Tin nhắn này sẽ KHÔNG hiện vì DEBUG < INFO")
logging.info("Chương trình bắt đầu chạy...")
logging.warning("Dung lượng đĩa sắp đầy!")
logging.error("Không thể mở file data.json")
logging.critical("Mất kết nối Cơ sở dữ liệu!")