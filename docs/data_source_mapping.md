# Data Source Mapping: Vnstock Free vs. Cào Nguồn Ngoài

> Tổng hợp từ `data_gap_analysis.md` + `pro_investor_data_gap.md`, đối chiếu `vnstock_free_data_fields.md`
> **Cập nhật 26/04/2026:** Đã chuyển các mục BCTC, Chỉ số tài chính, Sự kiện từ vnstock free sang cào ngoài do lỗi API từ nguồn cung cấp (KBS/VCI).

---

## PHẦN A: ✅ DỮ LIỆU ĐÃ CÓ TỪ VNSTOCK FREE

Những dữ liệu này **không cần cào bên ngoài**, dùng trực tiếp vnstock free hoặc tự tính.

### A1. Dữ liệu lấy trực tiếp (API call)

| # | Dữ liệu | Vnstock Module | Method | Fields chính |
|:---:|:---|:---|:---|:---|
| 1 | **OHLCV giá cổ phiếu** | `Quote` | `history(start, end, interval)` | `time`, `open`, `high`, `low`, `close`, `volume` |
| 2 | **Company name, ngành, lịch sử** | `Company` | `overview()` | `ticker`, `company_name`, `established_year`, `history`, `main_business` |
| 3 | **Danh sách cổ phiếu theo nhóm** | `Listing` | `symbols_by_group(group_name)` | VN30, VN100, HNX30... |
| 4 | **Ticker ↔ ngành mapping** | `Listing` | `symbols_by_industries()` | `symbol`, `industry_name` |
| 5 | **Cổ đông lớn** | `Company` | `shareholders()` | `name`, `share_type`, `quantity`, `percentage` |
| 6 | **Ban lãnh đạo + sở hữu** | `Company` | `officers()` | `name`, `position`, `ownership_pct` |
| 7 | **Giá vàng SJC** | `Misc` | — | `sjc_buy`, `sjc_sell` |
| 8 | **Tỷ giá VCB (hiện tại)** | `Misc` | — | `vcb_buy_cash`, `vcb_sell` |
| 9 | **VN-Index / VN30 index** | `Quote` | `history(symbol='VNINDEX')` | OHLCV chỉ số thị trường |
| 10 | **Intraday trades** | `Quote` | `intraday()` | `time`, `price`, `volume`, `side` |
| 11 | **Price board (realtime)** | `Quote` | `price_board()` (VCI) | `match_price`, `bid/ask`, `foreign_buy` |
| 12 | **Fund listing** | `Fund` | `listing(fund_type)` | `name`, `nav`, `nav_change_1m/3m/6m/12m` |
| 13 | **Phái sinh / Chứng quyền** | `Listing` | `derivatives()` / `warrants()` (VCI) | `symbol`, `underlying`, `expiration` |

### A2. Dữ liệu tự tính từ vnstock free (logic pipeline)

| # | Dữ liệu | Cách tính | Input |
|:---:|:---|:---|:---|
| 14 | **SMA, RSI, MACD** (indicators) | Tính deterministic từ OHLCV | `Quote.history()` |
| 15 | **Support / Resistance levels** | Pivot points từ OHLCV | `Quote.history()` |
| 16 | **Volume anomaly detection** | Statistical outlier detection từ OHLCV | `Quote.history()` |
| 17 | **Company summary (refined)** | LLM generate 1 lần từ `overview().history` | `Company.overview()` |
| 18 | **Audit log** | Tự sinh từ system runtime | Không cần data |
| 19 | **Ticker ↔ Macro mapping** | Tự build thủ công ~50 rules | Không cần cào |

> ⚠️ **Lưu ý:** Các mục tính toán dựa trên BCTC (Revenue growth, Peer Valuation, P/E Band, EV/EBITDA) hiện cần dữ liệu từ **PHẦN B** thay vì vnstock free.

---

## PHẦN B: ❌ DỮ LIỆU CẦN CÀO TỪ NGUỒN NGOÀI

Vnstock free **không cung cấp** (hoặc API bị hỏng) — phải tự cào, scrape hoặc download.

### B1. 🔴 Ưu tiên cao (Blocker)

| # | Dữ liệu | Agent cần | Nguồn cào | Phương pháp | Khối lượng |
|:---:|:---|:---|:---|:---|:---|
| **B1** | **Tin tức tài chính VN** | News & Sentiment | CafeF, Vietstock | RSS feed + Scraping | ≥ 6 tháng |
| **B2** | **BCTC PDF** (full-text) | Fundamental (RAG) | CafeF, VNDirect | Download PDF → OCR/Parse | 4 quý + 1 năm |
| **B3** | **Segment Revenue Breakdown** | Fundamental | BCTC thuyết minh | Parse table từ PDF/HTML | Top 100 tickers |
| **B4** | **Insider Transactions** | Management/KG | HOSE, CafeF | Scraping | Continuous |
| **B5** | **Foreign Flow lịch sử** | Smart Money | CafeF, Vietstock | Scraping time-series | ≥ 1-2 năm |
| **B6** | **Tỷ giá USD/VND lịch sử** | Risk/KG | SBV, FMP | API hoặc scraping | ≥ 2 năm |
| **B7** | **Nghị quyết ĐHCĐ** | Growth/KG | CafeF, IR page | Download PDF/HTML | 1-2 năm |
| **B21** | **Báo cáo tài chính (KQKD, Cân đối, LCTT)** | Fundamental | CafeF, Vietstock | Scrape HTML Table | Toàn bộ lịch sử |
| **B22** | **Chỉ số tài chính (P/E, P/B, ROE...)** | Fundamental | CafeF, Vietstock | Scrape HTML Table | Toàn bộ lịch sử |

### B2. 🟡 Ưu tiên trung bình

| # | Dữ liệu | Agent cần | Nguồn cào | Phương pháp | Khối lượng |
|:---:|:---|:---|:---|:---|:---|
| **B8** | **Analyst Reports** | Fundamental (RAG) | Website CTCK research | Download PDF → RAG | 5-10 per ticker |
| **B9** | **Lãi suất SBV / liên ngân hàng** | KG / Risk | sbv.gov.vn, CafeF | Scraping | ≥ 2 năm |
| **B10** | **Proprietary Trading Flow** | Smart Money | CafeF | Scraping | ≥ 1 năm |
| **B11** | **Fund Holdings** | Smart Money | Báo cáo NAV quỹ | Download PDF / scrape | Quarterly |
| **B12** | **Báo cáo ngành** | Growth/KG | CTCK Research | Download PDF → RAG | Theo ngành |
| **B13** | **CPI / Lạm phát VN** | Risk/KG | GSO, World Bank | API / scraping | Monthly |
| **B14** | **GDP growth VN** | Risk/KG | GSO, World Bank | API | Quarterly |
| **B15** | **Biên bản ĐHCĐ** | Growth/KG | HOSE, CafeF | Download PDF | 1-2 năm |
| **B23** | **Sự kiện doanh nghiệp (Cổ tức, niêm yết)** | KG / Events | CafeF, Vietstock | Scraping | Continuous |
| **B24** | **Thống kê GD (Market Cap, Beta, EPS, ICB)** | Indicator/KG | Vietstock, CafeF | Scraping | Daily |

### B3. 🟢 Ưu tiên thấp (Nice-to-have)

| # | Dữ liệu | Agent cần | Nguồn cào | Phương pháp |
|:---:|:---|:---|:---|:---|
| **B16** | **Earnings call transcripts** | Growth | IR pages, YouTube | Scraping / transcript API |
| **B17** | **IR page content** | Growth/Fundamental | Company IR websites | Scraping HTML/PDF |
| **B18** | **Thay đổi nhân sự cấp cao** | Management | News crawl | NLP pipeline |
| **B19** | **Giá dầu thế giới** | KG/Risk | MSN / FMP | API |
| **B20** | **VnExpress kinh doanh** | News | vnexpress.net | RSS feed |

---

## PHẦN C: TỔNG QUAN NHANH

```
┌─────────────────────────────────────────────────────┐
│  VNSTOCK FREE (19 data points)                      │
│  ✅ OHLCV, Company Info, Officers, Shareholders,    │
│     Gold/Forex, VN-Index, Indicators (tự tính)       │
│     → KHÔNG CẦN CÀO                                 │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  CẦN CÀO NGUỒN NGOÀI (24 data points)               │
│                                                     │
│  🔴 Cao (9):  Tin tức, BCTC PDF, BCTC Structured,   │
│     Chỉ số tài chính, Insider Trans, Foreign Flow,  │
│     USD/VND lịch sử, Nghị quyết ĐHCĐ, Breakdown     │
│                                                     │
│  🟡 TB (10):  Analyst Reports, Lãi suất SBV,        │
│     Tự doanh, Fund Holdings, Báo cáo ngành,         │
│     CPI/GDP, Biên bản, Sự kiện, Thống kê GD/ICB     │
│                                                     │
│  🟢 Thấp (5): Earnings call, IR page, Nhân sự,      │
│     Giá dầu, VnExpress                              │
└─────────────────────────────────────────────────────┘
```

---

## PHẦN D: NGUỒN CÀO GỘP THEO WEBSITE

| Website | Data có thể cào | IDs data | Ưu tiên | Lưu ý |
|:---|:---|:---:|:---:|:---|
| **CafeF** (cafef.vn) | Tin tức, BCTC PDF, BCTC Table, Ratios, Events, Insider Trans, Foreign Flow, Tự doanh, Lãi suất | B1,B2,B4,B5,B10,B7,B15,B9,B21,B22,B23 | 🔴 | RSS + Scraping, có WAF |
| **Vietstock** (vietstock.vn) | Tin tức, BCTC PDF, BCTC Table, Ratios, Events, Thống kê GD/ICB | B1,B2,B5,B21,B22,B23,B24 | 🔴 | Scraping, có WAF, cần login |
| **VNDirect** | BCTC PDF, Analyst Reports | B2,B8 | 🔴 | Public downloads |
| **HOSE / HNX** | Insider Trans, BCTC niêm yết, Biên bản | B4,B2,B15 | 🟡 | Format khó cào |
| **SSI / HSC Research**| Analyst Reports, Báo cáo ngành | B8,B12 | 🟡 | Cần đăng ký |
| **SBV / GSO** | Lãi suất, Tỷ giá, CPI, GDP | B9,B6,B13,B14 | 🔴 | Scraping / API |
| **Company IR pages** | Nghị quyết, Annual Report, Breakdown | B7,B16,B17,B3 | 🟡 | ~50 tickers |

---

> **Tổng kết:** Tỷ lệ phụ thuộc vào cào ngoài đã tăng lên (từ 40% lên ~55%) do các API cơ bản về tài chính và sự kiện của vnstock free không còn hoạt động ổn định.
