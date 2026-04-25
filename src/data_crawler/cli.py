import argparse
import sys
from pathlib import Path

# Add project root to path so we can import from .
sys.path.append(str(Path(__file__).parent.parent))

from data_crawler.main import crawl_ticker, main as run_batch
from data_crawler.config import TICKERS
from data_crawler.summary_generator import generate_summary
from data_crawler.logger import logger

def cli():
    parser = argparse.ArgumentParser(description="Vietstock Data Crawler CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Run crawler for all configured tickers")
    
    # Single ticker command
    single_parser = subparsers.add_parser("ticker", help="Run crawler for a specific ticker")
    single_parser.add_argument("symbol", type=str, help="Ticker symbol (e.g., FPT)")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Generate collection summary report")

    args = parser.parse_args()

    if args.command == "batch":
        run_batch()
    elif args.command == "ticker":
        logger.info(f"Starting crawler for single ticker: {args.symbol}")
        crawl_ticker(args.symbol.upper())
    elif args.command == "summary":
        logger.info("Generating summary report...")
        generate_summary()
        logger.info("Summary report generated: data_summary.md")
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
