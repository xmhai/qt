# qt

Quantitative trading for retail trader.

## Major functions
- Data
  - history data: OHLCV
  - fundamentals: PE, Dividend, Profit etc.
  - macro: interest rates, CPI, unemployment, yield curves, etc
- Feature Engineering
  - momentum scores, valuation ratios, yield-curve slope  
- Models
  - Mean reversion / momentum
  - can be as simple as a rules-based ranking system, or ML (gradient boosting, logistic regression)
- Backtesting
  - Include transaction cost
  - Use Out-of-Sample Testing: Hide a chunk of your historical data (e.g., 30%). Build your strategy on the first 70%, and test it on the hidden 30% only once.

## Biggest pitfalls specific to retail
Overfitting — with limited data and many free tools to "backtest until it looks good," it's easy to curve-fit noise
Survivorship bias in free datasets

## Technology Stack
- Python
- SQLite

## Strategy
- Factor investing + Momentum / trend following + Mean reversion + risk management
- Bank
  - macro: interest rates, CPI, unemployment, yield curves, etc
- REIT
- Technology

## Architecture
Market Data
    ↓
Data Storage
    ↓
Signal Calculation
    ↓
Portfolio / Position Sizing
    ↓
Risk Management
    ↓
Backtesting
    ↓
Paper Trading
    ↓
Broker API
    ↓
Live Trading

## Major Module
Data ingestion
Strategy interface
Backtesting engine
Portfolio simulator
Performance metrics
Parameter testing

## Data Ingestion

OHLCV history is pulled from Yahoo Finance (via `yfinance`) and stored in the SQLite
database configured by `DATABASE_URI` in [`src/config.py`](src/config.py). Tables are
defined in [`src/data/models.py`](src/data/models.py); the ingestion function lives in
[`src/data/data_ingestion.py`](src/data/data_ingestion.py).

Run directly as a script, from the project root or from `src/data/` — it locates the
`src` package automatically either way:

```bash
python src\data\data_ingestion.py "D05.SI"
python src\data\data_ingestion.py "AAPL" "JPM" "BAC"
```

With no date flags, it fetches the earliest available history through today
(`yfinance period="max"`). Pass `--start-date YYYY-MM-DD` / `--end-date YYYY-MM-DD` to
narrow the range:

```bash
python src\data\data_ingestion.py "D05.SI" --start-date 2024-01-01
```

It can also be called as a library function:

```bash
python -c "from src.data.data_ingestion import ingest_ohlcv; print(ingest_ohlcv(['JPM', 'BAC']))"
```

`ingest_ohlcv(symbols, start_date=None, end_date=None)` creates a `securities` row per
new symbol, inserts only dates not already stored (safe to re-run), and records each run
in `ingestion_log`.

### Symbol format for non-US exchanges

Yahoo Finance requires an exchange suffix for tickers outside the US. Use the local
exchange code, not the raw ticker:

| Exchange | Suffix | Example |
|---|---|---|
| SGX (Singapore) | `.SI` | DBS Group Holdings (D05) → `D05.SI` |
| HKEX (Hong Kong) | `.HK` | |
| LSE (London) | `.L` | |

To load DBS (SGX: D05), all history from the earliest available date:

```bash
python src\data\data_ingestion.py "D05.SI"
```

The `securities.symbol` column stores the Yahoo Finance symbol as-is (e.g. `D05.SI`),
and `ohlcv` prices are in the security's native currency (SGD for SGX-listed names) —
no FX conversion is applied during ingestion.

## Roadmap
Level 1
Simple rules
    ↓
Momentum / Value (liquidity) / Volatility

Level 2
Factor model
    ↓
Combine multiple signals

Level 3
Regularized linear model
    ↓
Ridge / Lasso / Elastic Net

Level 4
Tree-based ML
    ↓
XGBoost / LightGBM

Level 5
Neural networks
    ↓
Only if evidence justifies it
