import logging
from pathlib import Path 



def setup_logger() -> logging.Logger: 
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger("qa_builder")
    logger.setLevel(logging.INFO)

    if logger.handlers: 
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_dir / "run.log",
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger() 

logger.info("Bắt đầu chương trình")
logger.warning("File có dữ liệu thiếu")
logger.error("Không thể đọc file")
