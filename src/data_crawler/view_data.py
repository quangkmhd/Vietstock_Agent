import sys
import pandas as pd
from pathlib import Path

def preview_data(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File {file_path} not found.")
        return

    try:
        if path.suffix == ".parquet":
            df = pd.read_parquet(path)
        elif path.suffix == ".csv":
            df = pd.read_csv(path)
        else:
            print(f"Unsupported file format: {path.suffix}")
            return

        print(f"\n--- Previewing: {path.name} ---")
        print(f"Total rows: {len(df)}, Columns: {len(df.columns)}")
        print("\nFirst 5 rows:")
        print(df.head().to_string())
        print("-" * (len(path.name) + 20))
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/view_data.py <path_to_file>")
        sys.exit(1)
    
    preview_data(sys.argv[1])
