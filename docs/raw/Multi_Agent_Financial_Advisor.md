# Multi-Agent Financial Advisor System for Vietnam Market

## Overview
A comprehensive system designed to assist both retail and institutional investors in the Vietnamese financial market. The system utilizes multiple specialized agents coordinated by a central reasoning engine to provide grounded, data-driven investment advice.

## Core Philosophy
- **Reasoning with LLMs, Calculating with Code**: LLMs are used for intent recognition, planning, and synthesis. All technical calculations (indicators) and data retrievals are performed using deterministic code and verified data sources.
- **Micro-Agent Architecture**: Each agent is a specialized micro-service with a narrow scope and a specific set of tools.

## System Architecture

### 1. Gateway Layer (Router)
- **Role**: Receives user queries (natural language).
- **Functions**:
    - Intent classification (e.g., "Market Trend", "Company Deep Dive", "Technical Analysis").
    - Ticker extraction and mapping (e.g., "VCB" -> "VCB.VN").

### 2. Planning Layer (Planner/Orchestrator)
- **Role**: Breaks down complex intents into sequential or parallel tasks for specialized agents.
- **Mechanism**: ReAct (Reasoning and Acting) loops.

### 3. Agent Layer (Specialized Agents)

#### A. Market Agent
- **Focus**: Historical and real-time price action.
- **Tools**:
    - `get_ohlcv`: Fetches price/volume data.
    - `calculate_indicators`: Calculates SMA, RSI, MACD, etc.
- **Data Source**: Vnstock3 (Primary), Yfinance (Secondary).

#### B. Fundamental Agent
- **Focus**: Financial health and valuation.
- **Tools**:
    - `get_financial_statements`: Income statement, Balance sheet, Cash flow.
    - `get_valuation_ratios`: P/E, P/B, ROE.
- **Data Source**: Vnstock3, Vector Database (PDF Reports).

#### C. News & Sentiment Agent
- **Focus**: Market narrative and qualitative factors.
- **Tools**:
    - `search_news`: Scrapes recent headlines and summaries.
    - `analyze_sentiment`: Scores sentiment for specific tickers or sectors.

#### D. Knowledge Graph Agent
- **Focus**: Relationships and macro context.
- **Connections**: Ticker -> Sector -> Macro Factors (Interest rates, Oil prices).

### 4. Synthesis Layer (Advisor)
- **Role**: Aggregates findings from all agents.
- **Output**: A structured, cited investment report or answer.

## Data Workflow
1. **Extraction**: Automated scrapers and API integrations.
2. **Transformation**: Normalization into standard SQL and Vector formats.
3. **Loading**: Persistent storage in PostgreSQL (pgvector) and Object Storage.

## Key Performance Indicators (KPIs)
- **Accuracy**: 100% for technical indicators (verified via unit tests).
- **Latency**: End-to-end response < 10 seconds for simple queries.
- **Token Efficiency**: Aggressive caching of frequent data lookups.

## Security & Compliance
- **Data Privacy**: All user queries are anonymized before processing.
- **Compliance**: The advisor must provide a disclaimer that information is for educational purposes only.
- **Source Attribution**: All data points must be attributed to their original source.
