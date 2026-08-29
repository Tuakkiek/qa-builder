import logging

logging.basicConfig(level=logging.INFO)

logging.debug("Tin nhắn này sẽ KHÔNG hiện vì DEBUG < INFO")
logging.info("Chương trình bắt đầu chạy...")
logging.warning("Dung lượng đĩa sắp đầy!")
logging.error("Không thể mở file data.json")
logging.critical("Mất kết nối Cơ sở dữ liệu!")