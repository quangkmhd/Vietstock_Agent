import pandas as pd
from pathlib import Path
from .logger import write_download_log, logger
from .config import DATA_LAKE_DIR, SAVE_CSV, READABLE_DATA_DIR

def get_file_path(data_type: str, ticker: str, category: str = "", is_csv: bool = False) -> Path:
    base_dir = READABLE_DATA_DIR if is_csv else DATA_LAKE_DIR
    ext = "csv" if is_csv else "parquet"
    if category:
        return base_dir / data_type / category / f"{ticker}.{ext}"
    return base_dir / data_type / f"{ticker}.{ext}"

def check_exists(data_type: str, ticker: str, category: str = "") -> bool:
    file_path = get_file_path(data_type, ticker, category)
    return file_path.exists()

def save_data(df: pd.DataFrame, data_type: str, ticker: str, category: str = "", range_crawled: str = "Full") -> bool:
    if df is None or df.empty:
        write_download_log(ticker, f"{data_type}/{category}", range_crawled, 0, "success", "Empty dataframe")
        return False
        
    # Save Parquet (Standard format for pipeline)
    parquet_path = get_file_path(data_type, ticker, category, is_csv=False)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Force column names to string for Parquet compatibility
        df.columns = df.columns.astype(str)
        df.to_parquet(parquet_path, index=False)
        
        # Save CSV (Readable format for human)
        if SAVE_CSV:
            csv_path = get_file_path(data_type, ticker, category, is_csv=True)
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
        write_download_log(ticker, f"{data_type}/{category}", range_crawled, len(df), "success")
        return True
    except Exception as e:
        logger.error(f"Error saving {data_type}/{category} for {ticker}: {e}")
        write_download_log(ticker, f"{data_type}/{category}", range_crawled, 0, "fail", str(e))
        return False
