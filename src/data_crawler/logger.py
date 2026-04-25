import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .config import LOG_FILE

# Thiết lập logger xuất ra console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Crawler")

def write_download_log(ticker: str, data_type: str, range_crawled: str, rows_count: int, status: str, error_msg: str = ""):
    """
    Ghi log chi tiết tiến trình download vào file JSON
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ticker": ticker,
        "data_type": data_type,
        "range_crawled": range_crawled,
        "rows_count": rows_count,
        "status": status,
        "error": error_msg
    }
    
    # Read existing logs if exists
    logs = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
            
    logs.append(log_entry)
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)
