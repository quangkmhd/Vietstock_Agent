import time
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from vnstock import Quote, Company, Finance

from .config import MAX_RETRIES, RETRY_MIN_WAIT, RETRY_MAX_WAIT
from .logger import logger

# Retry decorator setup
def retry_logic():
    return retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=RETRY_MIN_WAIT, max=RETRY_MAX_WAIT),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )

@retry_logic()
def fetch_historical_price(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching historical price for {ticker}")
    quote = Quote(symbol=ticker)
    return quote.history(length="25Y", interval="1D")

# ------ COMPANY DATA ------
@retry_logic()
def fetch_company_overview(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching overview for {ticker}")
    return Company(source="KBS", symbol=ticker).overview()

@retry_logic()
def fetch_company_officers(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching officers for {ticker}")
    return Company(source="KBS", symbol=ticker).officers()

@retry_logic()
def fetch_company_shareholders(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching shareholders for {ticker}")
    return Company(source="KBS", symbol=ticker).shareholders()

@retry_logic()
def fetch_company_ownership(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching ownership for {ticker}")
    return Company(source="KBS", symbol=ticker).ownership()

@retry_logic()
def fetch_company_subsidiaries(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching subsidiaries for {ticker}")
    try:
        return Company(source="KBS", symbol=ticker).subsidiaries()
    except Exception as e:
        logger.warning(f"KBS subsidiaries failed for {ticker}, fallback to VCI. Error: {e}")
        return Company(source="VCI", symbol=ticker).subsidiaries()

@retry_logic()
def fetch_company_affiliate(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching affiliate for {ticker}")
    try:
        return Company(source="KBS", symbol=ticker).affiliate()
    except Exception as e:
        logger.warning(f"KBS affiliate failed for {ticker}, fallback to VCI. Error: {e}")
        return Company(source="VCI", symbol=ticker).affiliate()

@retry_logic()
def fetch_company_events(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching events for {ticker}")
    df = Company(source="KBS", symbol=ticker).events()
    if df is None or df.empty:
        logger.warning(f"KBS events empty for {ticker}, fallback to VCI.")
        try:
            df = Company(source="VCI", symbol=ticker).events()
        except Exception as e:
            logger.warning(f"VCI events also failed for {ticker}. Error: {e}")
            df = pd.DataFrame()
    return df

@retry_logic()
def fetch_company_news(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching news for {ticker}")
    return Company(source="KBS", symbol=ticker).news()

@retry_logic()
def fetch_company_capital_history(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching capital history for {ticker}")
    return Company(source="KBS", symbol=ticker).capital_history()

@retry_logic()
def fetch_company_insider_trading(ticker: str) -> pd.DataFrame:
    logger.info(f"Fetching insider trading for {ticker}")
    return Company(source="KBS", symbol=ticker).insider_trading()

# ------ FINANCIAL DATA ------
@retry_logic()
def fetch_financial_statement(ticker: str, statement_type: str, period: str) -> pd.DataFrame:
    logger.info(f"Fetching {statement_type} ({period}) for {ticker}")
    finance = Finance(source="kbs", symbol=ticker)
    
    if statement_type == "income_statement":
        return finance.income_statement(period=period)
    elif statement_type == "balance_sheet":
        return finance.balance_sheet(period=period)
    elif statement_type == "cash_flow":
        return finance.cash_flow(period=period)
    elif statement_type == "ratio":
        return finance.ratio(period=period)
    return pd.DataFrame()
