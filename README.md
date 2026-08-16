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
