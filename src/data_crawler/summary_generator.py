import json
import pandas as pd
from pathlib import Path

def generate_summary():
    log_file = Path("data_crawler/logs/download_log.json")
    if not log_file.exists():
        print("Log file not found.")
        return

    with open(log_file, "r") as f:
        logs = json.load(f)

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(logs)

    # Filter to only the latest attempt for each ticker and data_type combination
    df = df.sort_values("timestamp").drop_duplicates(["ticker", "data_type"], keep="last")

    total_files = len(df[df["status"] == "success"])
    total_records = df["rows_count"].sum()

    # Coverage by ticker
    coverage = df.groupby("ticker").agg(
        total_calls=("data_type", "count"),
        success_calls=("status", lambda x: (x == "success").sum()),
        total_rows=("rows_count", "sum")
    ).reset_index()

    # Missing/Failed data
    missing_data = df[df["status"] != "success"][["ticker", "data_type", "error"]]
    empty_data = df[(df["status"] == "success") & (df["rows_count"] == 0)][["ticker", "data_type", "error"]]

    with open("data_summary.md", "w") as f:
        f.write("# Data Collection Summary Report\n\n")
        f.write(f"**Total Files Collected:** {total_files}\n")
        f.write(f"**Total Records Collected:** {total_records}\n\n")

        f.write("## 1. Coverage by Ticker\n")
        f.write(coverage.to_markdown(index=False) + "\n\n")

        f.write("## 2. Empty Data (Successfully crawled but returned 0 rows)\n")
        if empty_data.empty:
            f.write("No empty data returned.\n\n")
        else:
            f.write(empty_data.to_markdown(index=False) + "\n\n")

        f.write("## 3. Missing/Failed Data\n")
        if missing_data.empty:
            f.write("No failures encountered during the final crawl.\n\n")
        else:
            f.write(missing_data.to_markdown(index=False) + "\n\n")

if __name__ == "__main__":
    generate_summary()
