import os
from pathlib import Path

# Thư mục gốc chứa dữ liệu
DATA_LAKE_DIR = Path("data_lake/raw")

from dotenv import load_dotenv

load_dotenv()

# Danh sách các mã cổ phiếu cần crawl
TICKERS = [
    "FPT", "HPG", "VCB", "MBB", "TCB", 
    "VNM", "VIC", "SSI", "VND", "MWG"
]

api_keys_str = os.getenv("VNSTOCK_API_KEYS", "")
API_KEYS = [k.strip() for k in api_keys_str.split(",")] if api_keys_str else []

# Load fallback from numbered variables (VNSTOCK_API_KEY_1, VNSTOCK_API_KEY_2...)
if not API_KEYS:
    for i in range(1, 20):
        key = os.getenv(f"VNSTOCK_API_KEY_{i}")
        if key:
            API_KEYS.append(key.strip())


# Các thiết lập Crawling
MAX_RETRIES = 1
RETRY_MIN_WAIT = 2
RETRY_MAX_WAIT = 10
SLEEP_BETWEEN_TICKERS = 2

# Log file
LOG_FILE = Path("data_crawler/logs/download_log.json")

# Readable format (for human review)
SAVE_CSV = True
READABLE_DATA_DIR = Path("data_lake/readable")
