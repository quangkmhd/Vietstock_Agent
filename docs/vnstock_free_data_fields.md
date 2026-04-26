# Vnstock Free-Tier Data Fields & Metadata Mapping (Official Guide Audit)

This document provides a comprehensive mapping of all data fields, parameters, and metadata available in the free version of the `vnstock` library (v3.x), cross-referenced with the official `vnstock-agent-guide`.

## 1. Core Entry Points
- **Modern (All-in-one):** `from vnstock import Vnstock`
  - `Vnstock().stock(symbol, source)` -> Access all company-specific modules.
  - `Vnstock().fx(symbol, source)` -> Forex data.
  - `Vnstock().crypto(symbol, source)` -> Crypto data.
  - `Vnstock().world_index(symbol, source)` -> Global indices.
- **Traditional (Modular):** `from vnstock import Listing, Company, Quote, Finance, Trading, Fund, Misc`

---

## 2. Listing Metadata (`vnstock.Listing`)
| Module/Method | Source | Key Parameters | Return Fields (Metadata) |
| :--- | :--- | :--- | :--- |
| `all_symbols()` | KBS, VCI | `to_df` | `symbol`, `exchange`, `short_name`, `company_type`, `industry`, `industry_id` |
| `industries_icb()` | VCI only | `lang` | `icb_id`, `icb_code`, `icb_name`, `super_group` |
| `symbols_by_industries()` | KBS, VCI | `to_df` | `symbol`, `industry_name` |
| `symbols_by_group()` | KBS, VCI | `group_name` | `symbol` (e.g. VN30, VN100, HNX30) |
| `indices_by_group()` | VCI, KBS | `group` | `symbol`, `name`, `type`, `exchange` |
| `derivatives()` | VCI | - | `symbol`, `underlying`, `expiration_date` |
| `warrants()` | VCI | - | `symbol`, `issuer`, `underlying`, `strike_price` |

---

## 3. Company Metadata (`vnstock.Company`)
| Module/Method | Source | Key Parameters | Return Fields (Metadata) |
| :--- | :--- | :--- | :--- |
| `overview()` | KBS, VCI | - | `ticker`, `company_name`, `established_year`, `employees`, `history`, `main_business` |
| `shareholders()` | KBS, VCI | - | `name`, `share_type`, `quantity`, `percentage` |
| `officers()` | KBS, VCI | - | `name`, `position`, `ownership_pct` |
| `events()` | KBS, VCI | - | `event_date`, `event_name`, `description` |
| `trading_stats()` | VCI only | - | `market_cap`, `free_float`, `beta`, `pe`, `pb`, `eps` |

---

## 4. Quote & Market Metadata (`vnstock.Quote`)
| Module/Method | Source | Key Parameters | Return Fields (Metadata) |
| :--- | :--- | :--- | :--- |
| `history()` | KBS, VCI, MSN | `start`, `end`, `interval` | `time`, `open`, `high`, `low`, `close`, `volume` |
| `intraday()` | KBS, VCI | `symbol`, `page_size` | `time`, `price`, `volume`, `side`, `match_type` |
| `price_board()` | VCI | `symbols` | `symbol`, `match_price`, `bid_price_1-3`, `ask_price_1-3`, `foreign_buy` |
| `price_board()` | KBS | `symbols` | `symbol`, `price`, `change`, `total_vol`, `total_val` |

---

## 5. Financial Metadata (`vnstock.Finance`)
- **Reports:** `income_statement()`, `balance_sheet()`, `cash_flow()`.
- **Ratios:** `ratio()` (46+ indicators: P/E, P/B, ROE, ROA, Debt/Equity, etc.).
- **Metadata Fields:** `item_id` (KBS), `levels`, `unit`, `row_number`.

---

## 6. Fund Data Metadata (`vnstock.Fund`)
| Module/Method | Source | Parameters | Return Fields (Metadata) |
| :--- | :--- | :--- | :--- |
| `listing()` | Fmarket | `fund_type` | `short_name`, `name`, `fund_owner_name`, `management_fee`, `nav`, `nav_change_1m/3m/6m/12m` |
| **Unsupported** | Fmarket | - | `details.overview()`, `details.nav_history()`, `details.holdings()` (Sponsored only) |

---

## 7. Visualization (`vnstock_chart`)
- **Library:** `vnstock_chart` (Built on `pyecharts`).
- **Features:** Professional financial charts (Candlestick, Line, Bar), dark/light themes, interaction tools (DataZoom, Tooltip).
- **Export:** `render()` (Auto-detect environment), `to_html()`, `embed()` (for Streamlit/Flask).

---

## 8. External Connectors (Free Tiers)
| Provider | Source Name | Description | Requires |
| :--- | :--- | :--- | :--- |
| **FMP** | `fmp` | Global data (AAPL, MSFT, Crypto, Macro) | Free API Key |
| **XNO** | `xno` | Vietnam market data for backtesting | Free API Key |
| **MSN** | `msn` | Global indices, Forex, Crypto | None |

---

## 9. Miscellaneous & Utilities
| Module | Feature | Metadata Fields |
| :--- | :--- | :--- |
| `Misc` | Gold & Forex | `sjc_buy`, `sjc_sell`, `vcb_buy_cash`, `vcb_sell` |
| `Proxy` | `ProxyManager` | `fetch_proxies()`, `get_best_proxy()`, `test_proxy()` |
| `Bot` | `Messenger` | Supports Telegram, Slack, LarkSuite webhooks |

---

## 10. Trading (DNSE Connector)
- **Account:** `account()`, `account_balance()`.
- **Orders:** `order_list()`, `deals_list()`.

---

> [!WARNING]
> **TCBS Source is Deprecated**: Do not use `source='tcbs'`. It is unstable for free users and requires authentication. Use **VCI** or **KBS** instead.
> **Screener API**: Currently inactive for free users due to source changes.
