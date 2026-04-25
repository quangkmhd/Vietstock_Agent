import time
from .config import TICKERS, SLEEP_BETWEEN_TICKERS, API_KEYS
from vnstock.core.utils.auth import change_api_key
from .fetcher import (
    fetch_historical_price,
    fetch_company_overview, fetch_company_officers, fetch_company_shareholders,
    fetch_company_ownership, fetch_company_subsidiaries, fetch_company_affiliate,
    fetch_company_events, fetch_company_news, fetch_company_capital_history,
    fetch_company_insider_trading, fetch_financial_statement
)
from .storage import check_exists, save_data
from .logger import logger

def crawl_ticker(ticker: str):
    logger.info(f"========== STARTING TICKER: {ticker} ==========")
    
    # 1. Historical Price
    if not check_exists("price", ticker, "history"):
        time.sleep(0.1)  # Đảm bảo không dính rate limit
        try:
            df_price = fetch_historical_price(ticker)
            save_data(df_price, "price", ticker, "history", range_crawled="2000-now")
        except BaseException as e:
            logger.error(f"Failed to fetch price for {ticker}: {e}")
    else:
        logger.info(f"Skip price/history for {ticker} (already exists)")
        
    # 2. Company Data
    company_methods = {
        "overview": fetch_company_overview,
        "officers": fetch_company_officers,
        "shareholders": fetch_company_shareholders,
        "ownership": fetch_company_ownership,
        "subsidiaries": fetch_company_subsidiaries,
        "affiliate": fetch_company_affiliate,
        "events": fetch_company_events,
        "news": fetch_company_news,
        "capital_history": fetch_company_capital_history,
        "insider_trading": fetch_company_insider_trading,
    }
    
    for category, fetch_func in company_methods.items():
        if not check_exists("company", ticker, category):
            time.sleep(0.1)
            try:
                df = fetch_func(ticker)
                save_data(df, "company", ticker, category)
            except BaseException as e:
                logger.error(f"Failed to fetch company/{category} for {ticker}: {e}")
        else:
            logger.info(f"Skip company/{category} for {ticker} (already exists)")

    # 3. Financial Data
    financial_types = ["income_statement", "balance_sheet", "cash_flow", "ratio"]
    periods = ["year", "quarter"]
    
    for stmt_type in financial_types:
        for period in periods:
            category = f"{stmt_type}_{period}"
            if not check_exists("finance", ticker, category):
                time.sleep(0.1)
                try:
                    df = fetch_financial_statement(ticker, stmt_type, period)
                    save_data(df, "finance", ticker, category)
                except BaseException as e:
                    logger.error(f"Failed to fetch finance/{category} for {ticker}: {e}")
            else:
                logger.info(f"Skip finance/{category} for {ticker} (already exists)")
                
    logger.info(f"========== FINISHED TICKER: {ticker} ==========")

def main():
    logger.info("Starting Batch Crawler...")
    for i, ticker in enumerate(TICKERS):
        api_key = API_KEYS[i % len(API_KEYS)]
        change_api_key(api_key)
        logger.info(f"Using API Key: {api_key} for {ticker}")
        
        crawl_ticker(ticker)
        logger.info(f"Sleeping for {SLEEP_BETWEEN_TICKERS}s before next ticker...")
        time.sleep(SLEEP_BETWEEN_TICKERS)
    logger.info("Batch Crawler Completed.")

if __name__ == "__main__":
    main()
