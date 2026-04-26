import os
import sys
import logging
import pandas as pd
from datetime import datetime

# Thêm đường dẫn để có thể import vnstock_auth nếu chạy trực tiếp
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# vnstock modules (Free version)
from vnstock import Quote, Company, Listing, Finance, Trading, Fund
from vnstock_auth import with_key_fallback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RAW_DATA_DIR = "data/raw/vnstock"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

def save_data(df: pd.DataFrame, category: str, filename: str):
    """Lưu DataFrame xuống file Parquet (ưu tiên) hoặc CSV."""
    if df is None or df.empty:
        logger.warning(f"Không có dữ liệu để lưu: {category}/{filename}")
        return
        
    category_dir = os.path.join(RAW_DATA_DIR, category)
    os.makedirs(category_dir, exist_ok=True)
    
    filepath = os.path.join(category_dir, filename)
    try:
        # Cố gắng lưu dưới định dạng Parquet để tối ưu không gian và tốc độ
        parquet_path = filepath if filepath.endswith('.parquet') else filepath + '.parquet'
        df.to_parquet(parquet_path, index=False)
        logger.info(f"Đã lưu {len(df)} dòng vào {parquet_path}")
    except Exception as e:
        logger.error(f"Không thể lưu Parquet. Thử lưu CSV. Lỗi: {e}")
        csv_path = filepath.replace('.parquet', '.csv') if filepath.endswith('.parquet') else filepath + '.csv'
        df.to_csv(csv_path, index=False)
        logger.info(f"Đã lưu {len(df)} dòng vào {csv_path}")

class VnstockDataCrawler:
    """
    Class quản lý việc tải dữ liệu Phần A1 từ vnstock (free).
    Các method sử dụng @with_key_fallback() để tự động đổi API key nếu bị rate limit.
    """
    def __init__(self, symbol="VCI"):
        self.symbol = symbol

    @with_key_fallback()
    def get_price_history(self):
        return Quote(source="KBS", symbol=self.symbol).history(start="2024-01-01", end=datetime.now().strftime("%Y-%m-%d"))

    @with_key_fallback()
    def get_intraday(self):
        return Quote(source="KBS", symbol=self.symbol).intraday()

    @with_key_fallback()
    def get_price_board(self):
        return Trading(source="KBS", symbol=self.symbol).price_board(symbols_list=[self.symbol])

    @with_key_fallback()
    def get_vnindex(self):
        return Quote(source="KBS", symbol="VNINDEX").history(start="2024-01-01", end=datetime.now().strftime("%Y-%m-%d"))

    @with_key_fallback()
    def get_company_overview(self):
        return Company(source="KBS", symbol=self.symbol).overview()

    @with_key_fallback()
    def get_shareholders(self):
        return Company(source="KBS", symbol=self.symbol).shareholders()

    @with_key_fallback()
    def get_officers(self):
        return Company(source="KBS", symbol=self.symbol).officers()

    @with_key_fallback()
    def get_fund_listing(self):
        return Fund().listing()

    @with_key_fallback()
    def get_symbols_by_group(self, group="VN30"):
        return Listing(source="KBS").symbols_by_group(group)

    @with_key_fallback()
    def get_symbols_by_industries(self):
        return Listing(source="KBS").symbols_by_industries()

def download_market_data(crawler):
    """Tải dữ liệu chung của toàn thị trường (chỉ cần chạy 1 lần)"""
    logger.info("--- Tải dữ liệu chung Thị trường (Market-wide) ---")
    save_data(crawler.get_vnindex(), "quote", "VNINDEX_history.parquet")
    save_data(crawler.get_symbols_by_group("VN30"), "listing", "symbols_VN30.parquet")
    save_data(crawler.get_symbols_by_industries(), "listing", "symbols_by_industries.parquet")
    save_data(crawler.get_fund_listing(), "listing", "fund_listing.parquet")

def run_pipeline_for_symbol(symbol):
    """Tải dữ liệu cho 1 mã cổ phiếu cụ thể"""
    logger.info(f"Đang xử lý mã: {symbol}...")
    crawler = VnstockDataCrawler(symbol=symbol)
    
    # 1. Dữ liệu Market (Giá cổ phiếu)
    save_data(crawler.get_price_history(), "quote", f"{symbol}_history.parquet")
    save_data(crawler.get_intraday(), "quote", f"{symbol}_intraday.parquet")
    save_data(crawler.get_price_board(), "quote", f"{symbol}_price_board.parquet")
    
    # 2. Thông tin doanh nghiệp
    save_data(crawler.get_company_overview(), "company", f"{symbol}_overview.parquet")
    save_data(crawler.get_shareholders(), "company", f"{symbol}_shareholders.parquet")
    save_data(crawler.get_officers(), "company", f"{symbol}_officers.parquet")

def main():
    import time
    logger.info("BẮT ĐẦU QUY TRÌNH TẢI DỮ LIỆU VNSTOCK FREE")
    
    # 1. Tải dữ liệu chung trước
    base_crawler = VnstockDataCrawler("VNINDEX")
    download_market_data(base_crawler)
    
    # 2. Lấy danh sách VN30
    vn30_series = base_crawler.get_symbols_by_group("VN30")
    if vn30_series is None or vn30_series.empty:
        logger.error("Không thể lấy danh sách VN30. Dừng chương trình.")
        return
        
    vn30_symbols = vn30_series.tolist()
    logger.info(f"Đã lấy được {len(vn30_symbols)} mã VN30: {vn30_symbols}")
    
    # 3. Lặp qua từng mã để tải dữ liệu
    for i, symbol in enumerate(vn30_symbols):
        logger.info(f"[{i+1}/{len(vn30_symbols)}] Bắt đầu tải dữ liệu cho {symbol}")
        run_pipeline_for_symbol(symbol)
        
        # Nghỉ 2 giây giữa các mã để tránh bị block IP
        if i < len(vn30_symbols) - 1:
            time.sleep(2)

    logger.info("🎉 HOÀN TẤT PIPELINE TẢI DỮ LIỆU PHẦN A1 CHO VN30.")

if __name__ == "__main__":
    main()
