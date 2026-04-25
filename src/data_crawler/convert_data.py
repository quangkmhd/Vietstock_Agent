import os
import pandas as pd
from pathlib import Path

def convert_parquet_to_csv(raw_dir, output_dir):
    """
    Recursively finds all .parquet files in raw_dir and converts them to .csv in output_dir.
    Maintains the same directory structure.
    """
    raw_path = Path(raw_dir)
    output_path = Path(output_dir)
    
    if not raw_path.exists():
        print(f"Error: Raw directory {raw_dir} does not exist.")
        return

    # Get all .parquet files recursively
    parquet_files = list(raw_path.rglob("*.parquet"))
    
    if not parquet_files:
        print(f"No .parquet files found in {raw_dir}")
        return

    print(f"Found {len(parquet_files)} parquet files. Starting conversion...")
    
    for parquet_file in parquet_files:
        # Calculate relative path to maintain structure
        rel_path = parquet_file.relative_to(raw_path)
        # Create corresponding CSV path
        csv_file = output_path / rel_path.with_suffix(".csv")
        
        # Create output directory if it doesn't exist
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Read parquet and save to CSV
            # Using utf-8-sig for Excel compatibility with Vietnamese characters if any
            df = pd.read_parquet(parquet_file)
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            print(f"✅ Converted: {rel_path}")
        except Exception as e:
            print(f"❌ Error converting {rel_path}: {e}")

if __name__ == "__main__":
    # Get the absolute path of the project root
    PROJECT_ROOT = Path(__file__).parent.parent.absolute()
    RAW_DATA_DIR = PROJECT_ROOT / "data_lake/raw"
    READABLE_DATA_DIR = PROJECT_ROOT / "data_lake/readable"
    
    convert_parquet_to_csv(RAW_DATA_DIR, READABLE_DATA_DIR)
    print(f"\nDone! You can find the readable CSV files in: {READABLE_DATA_DIR}")
