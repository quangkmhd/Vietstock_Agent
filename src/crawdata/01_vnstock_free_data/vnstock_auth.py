import os
import time
import logging
from functools import wraps
from dotenv import load_dotenv

# vnstock free's change_api_key
try:
    from vnstock.core.utils.auth import change_api_key
except ImportError:
    # Nếu không tìm thấy module auth trong vnstock, định nghĩa hàm rỗng để script không crash
    def change_api_key(key):
        pass

logger = logging.getLogger(__name__)

class APIKeyManager:
    def __init__(self):
        load_dotenv()
        self.keys = []
        # Đọc các key VNSTOCK_API_KEY_1 đến VNSTOCK_API_KEY_5 từ .env
        for i in range(1, 6):
            key = os.getenv(f"VNSTOCK_API_KEY_{i}")
            if key:
                self.keys.append(key)
        
        self.current_index = 0
        if not self.keys:
            logger.warning("Không tìm thấy VNSTOCK_API_KEY nào trong file .env")
        else:
            self._set_current_key()

    def _set_current_key(self):
        if self.keys:
            key = self.keys[self.current_index]
            try:
                change_api_key(key)
                logger.info(f"Đã chuyển sang API Key {self.current_index + 1}")
            except Exception as e:
                logger.warning(f"Không thể đổi API key: {e}")

    def rotate_key(self):
        if not self.keys:
            return False
        
        self.current_index = (self.current_index + 1) % len(self.keys)
        self._set_current_key()
        return True

key_manager = APIKeyManager()

def with_key_fallback(max_retries_per_key=3):
    """
    Decorator tự động thử lại (retry) và xoay vòng API key khi bị lỗi Rate Limit (429).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            total_keys = len(key_manager.keys) if key_manager.keys else 1
            for key_attempt in range(total_keys):
                for attempt in range(max_retries_per_key):
                    try:
                        return func(self, *args, **kwargs)
                    except SystemExit as e:
                        # vnstock often calls sys.exit(1) when rate limited instead of raising an exception
                        logger.warning(f"Lỗi Rate Limit (bị SystemExit). (lần thử {attempt + 1})")
                        if attempt < max_retries_per_key - 1:
                            time.sleep(2 ** attempt)
                            continue
                        else:
                            logger.info("Đã đạt giới hạn số lần thử, tiến hành đổi API key...")
                            key_manager.rotate_key()
                            break
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "429" in error_msg or "rate limit" in error_msg or "too many requests" in error_msg:
                            logger.warning(f"Lỗi Rate Limit (lần thử {attempt + 1}). Lỗi: {e}")
                            if attempt < max_retries_per_key - 1:
                                time.sleep(2 ** attempt)  # Exponential backoff
                                continue
                            else:
                                logger.info("Đã đạt giới hạn số lần thử, tiến hành đổi API key...")
                                key_manager.rotate_key()
                                break  # Thoát vòng lặp hiện tại để thử với key mới
                        else:
                            # Nếu không phải lỗi Rate Limit, trả về DataFrame rỗng thay vì crash
                            logger.error(f"Lỗi không phải Rate Limit khi gọi {func.__name__}: {e}")
                            import pandas as pd
                            return pd.DataFrame()
            logger.error("Đã thử hết tất cả API keys hoặc số lần thử.")
            return None
        return wrapper
    return decorator
