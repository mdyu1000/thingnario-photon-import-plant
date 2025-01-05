import logging
import sys
from pathlib import Path


def setup_logger():
    # 創建 logs 目錄（如果不存在）
    Path("logs").mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/power_station_converter.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger
