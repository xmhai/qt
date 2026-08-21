import sys
from datetime import date
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import yfinance as yf

from src.data.models import IngestionLog, OHLCV, SessionLocal, Security, init_db


def _get_or_create_security(session, symbol: str) -> Security:
    security = session.query(Security).filter_by(symbol=symbol).one_or_none()
    if security is None:
        security = Security(symbol=symbol)
        session.add(security)
        session.flush()
    return security


def ingest_ohlcv(
    symbols: list[str], start_date: str | None = None, end_date: str | None = None
) -> dict[str, int]:
    """Fetch daily OHLCV history from yfinance and upsert into the `ohlcv` table.

    If `start_date` is omitted, the earliest available history for each symbol is
    retrieved (yfinance `period="max"`).

    Returns a dict of symbol -> rows ingested.
    """
    init_db()
    session = SessionLocal()
    results: dict[str, int] = {}

    try:
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                if start_date is None:
                    history = ticker.history(period="max", auto_adjust=False)
                else:
                    history = ticker.history(
                        start=start_date, end=end_date, auto_adjust=False
                    )

                security = _get_or_create_security(session, symbol)

                existing_dates = {
                    row.date
                    for row in session.query(OHLCV.date).filter_by(security_id=security.id).all()
                }

                rows_ingested = 0
                for row_date, row in history.iterrows():
                    row_date = row_date.date()
                    if row_date in existing_dates:
                        continue
                    session.add(
                        OHLCV(
                            security_id=security.id,
                            date=row_date,
                            open=row["Open"],
                            high=row["High"],
                            low=row["Low"],
                            close=row["Close"],
                            adj_close=row.get("Adj Close", row["Close"]),
                            volume=int(row["Volume"]) if row["Volume"] == row["Volume"] else None,
                        )
                    )
                    rows_ingested += 1

                session.commit()
                results[symbol] = rows_ingested
                session.add(
                    IngestionLog(
                        source="yfinance",
                        target_table="ohlcv",
                        ref=symbol,
                        start_date=date.fromisoformat(start_date) if start_date else None,
                        end_date=date.fromisoformat(end_date) if end_date else None,
                        status="success",
                        rows_ingested=rows_ingested,
                    )
                )
                session.commit()
            except Exception as exc:
                session.rollback()
                session.add(
                    IngestionLog(
                        source="yfinance",
                        target_table="ohlcv",
                        ref=symbol,
                        start_date=date.fromisoformat(start_date) if start_date else None,
                        end_date=date.fromisoformat(end_date) if end_date else None,
                        status="failed",
                        rows_ingested=0,
                        error_message=str(exc),
                    )
                )
                session.commit()
                results[symbol] = 0
    finally:
        session.close()

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest daily OHLCV history for one or more symbols (earliest available date by default)."
    )
    parser.add_argument("symbols", nargs="+", help='Ticker symbol(s), e.g. "D05.SI" "AAPL"')
    parser.add_argument("--start-date", default=None, help="YYYY-MM-DD (default: earliest available)")
    parser.add_argument("--end-date", default=None, help="YYYY-MM-DD (default: latest available)")
    args = parser.parse_args()

    print(ingest_ohlcv(args.symbols, start_date=args.start_date, end_date=args.end_date))
