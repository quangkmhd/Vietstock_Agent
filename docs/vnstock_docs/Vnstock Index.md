---
title: 'Vnstock Documentation: AI Index & Mapping Guide'
tags:
- vnstock
- documentation
aliases:
- Vnstock Index
---

# Vnstock Documentation: AI Index & Mapping Guide

This file serves as a comprehensive index for AI agents to navigate the `docs/vnstock_docs` directory. It maps architectural layers, features, and modules of the Vnstock ecosystem to their corresponding local markdown files. 

**Always consult this index before trying to guess which documentation file to read for a specific task.**

---

## 1. Core Architecture & Foundations (Unified UI v3)
The V3 "Unified UI" architecture is the modern standard for querying data, abstracting specific providers (VCI, MAS, KBS) into logical layers.

* **Library Architecture & Design:** [[vnstocks.com_docs_vnstock-data_kien-truc-thu-vien]]
  * *Use when:* Understanding the foundational design philosophy, method chaining, the 7-layer architecture, and `show_api()` discovery function.
* **Market Layer:** [[vnstocks.com_docs_vnstock-data_market-layer-v3]]
  * *Use when:* Fetching historical prices (OHLCV), intraday tick data, real-time quotes, order book depths, or tracking institutional/foreign trading flows. (Methods: `ohlcv()`, `quote()`, `trades()`)
* **Reference Layer:** [[vnstocks.com_docs_vnstock-data_reference-layer-v3]]
  * *Use when:* Looking up stock symbols, corporate structures, shareholder lists, industry classifications, or market event calendars. (Methods: `info()`, `list()`, `calendar()`)
* **Fundamental Layer:** [[vnstocks.com_docs_vnstock-data_fundamental-layer-v3]]
  * *Use when:* Extracting quarterly/annual financial statements, evaluating financial health, or calculating EPS/ROE/Debt-to-Equity ratios.
* **Analytics Layer:** [[vnstocks.com_docs_vnstock-data_analytics-layer-v3]]
  * *Use when:* Performing market-wide valuation analyses, tracking broad historical index P/E and P/B ratios.
* **Macro Layer:** [[vnstocks.com_docs_vnstock-data_macro-layer-v3]]
  * *Use when:* Querying national economic indicators (GDP, CPI, FDI) or global commodity and currency exchange rates (e.g., gold, crude oil, USD/VND).
* **Insights Layer:** [[vnstocks.com_docs_vnstock-data_insights-layer-v3]]
  * *Use when:* Building stock screeners, identifying top market gainers/losers, tracking top movers, and finding investment opportunities.

---

## 2. Legacy / V2 Core APIs
If maintaining or migrating older codebase segments, refer to these earlier files (01-12 sequence and specific modules).

* **01 - 12 General Guides:** [[01-overview]], [[02-installation]], [[10-connector-guide]], [[11-best-practices]], [[12-migration-guide]]
* **V2 API Domains:**
  * Listing API: [[03-listing-api]], [[vnstocks.com_docs_vnstock_thong-tin-niem-yet]]
  * Company API: [[04-company-api]], [[vnstocks.com_docs_vnstock_thong-tin-cong-ty]]
  * Trading / Prices: [[05-trading-api]], [[06-quote-price-api]], [[vnstocks.com_docs_vnstock_thong-ke-gia-lich-su]], [[vnstocks.com_docs_vnstock_bang-gia-giao-dich]]
  * Financial API: [[07-financial-api]], [[vnstocks.com_docs_vnstock_bao-cao-tai-chinh]]
  * Fund / Screener API: [[08-fund-api]], [[09-screener-api]], [[vnstocks.com_docs_vnstock_bo-loc-co-phieu-vnstock]]
  * Macro Data: [[vnstocks.com_docs_vnstock_du-lieu-quy-mo]], [[vnstocks.com_docs_vnstock_du-lieu-thi-truong-hang-hoa]]

---

## 3. Quantitative Analysis & Trading (Vnstock TA)
* **Introduction & Overview:** [[vnstocks.com_docs_vnstock-ta_gioi-thieu]]
* **Usage Steps & Indicators:** [[vnstocks.com_docs_vnstock-ta_cac-buoc-su-dung]]
  * *Use when:* Calculating over 20 standard technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands) or generating interactive technical charts for quantitative analysis.

---

## 4. Automated Trading via DNSE
* **DNSE Trading API:** [[vnstocks.com_docs_vnstock_api-dat-lenh-giao-dich-dnse]]
  * *Use when:* Building automated bots to authenticate, query account balances, place, modify, or cancel equity and derivative orders via the DNSE API.

---

## 5. News Scraping & Parsing (Vnstock News)
* **General Usage:** [[vnstocks.com_docs_vnstock-news_gioi-thieu]], [[vnstocks.com_docs_vnstock-news_huong-dan-co-ban]]
* **Advanced Usage & Implementation:** [[vnstocks.com_docs_vnstock-news_tuy-bien-nang-cao]], [[vnstocks.com_docs_vnstock-news_mau-chuong-trinh-cap-nhat-tin-tuc]], [[vnstocks.com_docs_vnstock-news_vi-du-thuc-te]]
  * *Use when:* Building automated scrapers for 21+ major Vietnamese financial news websites (via RSS/Sitemaps) or collecting clean Markdown news data to train NLP/LLM models.

---

## 6. Data Pipeline & Automation (Vnstock Pipeline)
* **Overview & Storage:** [[vnstocks.com_docs_vnstock-pipeline_gioi-thieu]], [[vnstocks.com_docs_vnstock-pipeline_luu-tru-du-lieu-toi-uu]]
* **Realtime Data (WebSocket):** [[vnstocks.com_docs_vnstock-pipeline_ket-noi-du-lieu-realtime]]
* **Advanced Automation:** [[vnstocks.com_docs_vnstock-pipeline_tuy-chinh-pipeline]], [[vnstocks.com_docs_vnstock-pipeline_mau-nhiem-vu-tai-du-lieu-thong-dung]], [[vnstocks.com_docs_vnstock-pipeline_hieu-nang-toi-uu]]
  * *Use when:* Configuring asynchronous batch downloads, converting data to Parquet/DuckDB, setting up scheduled data extractors, or connecting to real-time market WebSockets.

---

## 7. AI, Utilities & Integrations
* **Data Visualization (ezchart):** [[vnstocks.com_docs_vnstock_bieu-dien-du-lieu]]
  * *Use when:* Using `vnstock_ezchart` to render timeseries, heatmaps, boxplots, and wordclouds.
* **Google Gemini AI Integration:** [[vnstocks.com_docs_vnstock_google-gemini-ai-flash-phan-tich-du-lieu-vnstock]]
  * *Use when:* Using the `gemini_ai` wrapper to automate data analysis and chart interpretations.
* **Messaging Bots (Telegram/Slack/Lark):** [[vnstocks.com_docs_vnstock_gui-tin-nhan-telegram-slack-larksuite]]
  * *Use when:* Setting up API webhooks for automated system alerts or daily stock reports.
* **Cloud & Proxy Utilities:** [[vnstocks.com_docs_vnstock_huong-dan-vnstock-proxy-manager]], [[vnstocks.com_docs_vnstock_luu-tru-vnstock-vao-google-drive-google-colab]]
  * *Use when:* Bypassing rate-limiting via ProxyManager or configuring Google Colab with persistent Google Drive storage.

---

## 8. Ecosystem & Sponsor
* **Sponsor Tiers & Access:** [[vnstocks.com_docs_vnstock-insider-api_index]]
* **Version History & Changes:** [[vnstocks.com_docs_vnstock-insider-api_lich-su-phien-ban]] (and [[vnstocks.com_docs_tai-lieu_lich-su-phien-ban]])
  * *Use when:* Checking requirements for Insider APIs (Bronze, Silver, Golden) or reading release notes for breaking changes and migration guides.