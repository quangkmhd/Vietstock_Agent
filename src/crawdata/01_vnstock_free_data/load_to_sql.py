import os
import glob
import logging
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load biến môi trường
load_dotenv()

# Lấy DATABASE_URL từ .env (Ưu tiên PostgreSQL: postgresql://user:pass@localhost:5432/vietstock)
# Nếu không có sẵn Postgres, dùng SQLite local (vietstock.db) làm nơi lưu trữ mặc định.
# Cả 2 loại CSDL này đều được LangChain hỗ trợ tuyệt đối qua SQLAlchemy.
DB_URL = os.getenv("DATABASE_URL", "sqlite:///data/vietstock.db")
logger.info(f"Khởi tạo kết nối tới Database: {DB_URL}")
engine = create_engine(DB_URL)

RAW_DIR = "data/raw/vnstock"

def load_and_merge_parquet(folder_path, pattern):
    """
    Đọc tất cả các file parquet trong thư mục raw, 
    gộp thành 1 DataFrame duy nhất để đẩy lên Database.
    """
    search_path = os.path.join(RAW_DIR, folder_path, pattern)
    files = glob.glob(search_path)
    
    if not files:
        logger.warning(f"Không tìm thấy file nào khớp với {search_path}")
        return pd.DataFrame()
        
    df_list = []
    for f in files:
        try:
            df = pd.read_parquet(f)
            # Thêm cột symbol vào nếu file đó không có nhưng tên file có (phòng hờ)
            # VD: VCI_history.parquet -> symbol là VCI
            filename = os.path.basename(f)
            if "_" in filename:
                symbol = filename.split("_")[0]
                if 'symbol' not in df.columns and symbol != "VNINDEX" and symbol != "symbols":
                    df['symbol'] = symbol
            df_list.append(df)
        except Exception as e:
            logger.error(f"Lỗi đọc file {f}: {e}")
            
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    return pd.DataFrame()

def load_to_database():
    logger.info("BẮT ĐẦU ĐẨY DỮ LIỆU TỪ RAW LAYER (PARQUET) LÊN SQL DATABASE...")
    
    # ---------------------------------------------------------
    # 1. BẢNG QUOTE (Lịch sử giá - Fact Table)
    # ---------------------------------------------------------
    logger.info("1. Đang xử lý bảng Lịch sử giá (daily_quotes)...")
    df_history = load_and_merge_parquet("quote", "*_history.parquet")
    if not df_history.empty:
        # Xóa duplicate nếu có (dựa trên mã CK và thời gian)
        if 'symbol' in df_history.columns and 'time' in df_history.columns:
            df_history = df_history.drop_duplicates(subset=['symbol', 'time'])
        df_history.to_sql('daily_quotes', engine, if_exists='replace', index=False)
        logger.info(f"   -> Đã gộp và đẩy {len(df_history)} dòng vào bảng 'daily_quotes'")

    # Bảng Intraday (Có thể chứa hàng chục ngàn dòng)
    logger.info("2. Đang xử lý bảng Giá trong ngày (intraday_quotes)...")
    df_intraday = load_and_merge_parquet("quote", "*_intraday.parquet")
    if not df_intraday.empty:
        df_intraday.to_sql('intraday_quotes', engine, if_exists='replace', index=False)
        logger.info(f"   -> Đã gộp và đẩy {len(df_intraday)} dòng vào bảng 'intraday_quotes'")

    # ---------------------------------------------------------
    # 2. BẢNG COMPANY (Hồ sơ công ty - Dimension Table)
    # ---------------------------------------------------------
    logger.info("3. Đang xử lý bảng Hồ sơ công ty (company_overview)...")
    df_overview = load_and_merge_parquet("company", "*_overview.parquet")
    if not df_overview.empty:
        # Mỗi mã CK (symbol) chỉ có 1 dòng overview
        if 'symbol' in df_overview.columns:
            df_overview = df_overview.drop_duplicates(subset=['symbol'])
        df_overview.to_sql('company_overview', engine, if_exists='replace', index=False)
        logger.info(f"   -> Đã gộp và đẩy {len(df_overview)} công ty vào bảng 'company_overview'")

    logger.info("4. Đang xử lý bảng Ban lãnh đạo (company_officers)...")
    df_officers = load_and_merge_parquet("company", "*_officers.parquet")
    if not df_officers.empty:
        df_officers.to_sql('company_officers', engine, if_exists='replace', index=False)
        logger.info(f"   -> Đã gộp và đẩy {len(df_officers)} dòng vào bảng 'company_officers'")

    logger.info("5. Đang xử lý bảng Cổ đông lớn (company_shareholders)...")
    df_shareholders = load_and_merge_parquet("company", "*_shareholders.parquet")
    if not df_shareholders.empty:
        df_shareholders.to_sql('company_shareholders', engine, if_exists='replace', index=False)
        logger.info(f"   -> Đã gộp và đẩy {len(df_shareholders)} dòng vào bảng 'company_shareholders'")

    # ---------------------------------------------------------
    # 3. BẢNG LISTING (Danh mục ngành/rổ/quỹ)
    # ---------------------------------------------------------
    logger.info("6. Đang xử lý bảng Danh mục ngành (market_listings)...")
    df_industries = load_and_merge_parquet("listing", "symbols_by_industries.parquet")
    if not df_industries.empty:
        df_industries.to_sql('market_listings', engine, if_exists='replace', index=False)
        logger.info(f"   -> Đã gộp và đẩy {len(df_industries)} dòng vào bảng 'market_listings'")

    logger.info("🎉 HOÀN TẤT QUÁ TRÌNH TẠO DATABASE CHO LANGCHAIN AI AGENT!")

if __name__ == "__main__":
    load_to_database()