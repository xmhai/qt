from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from src.config import DATABASE_URI

Base = declarative_base()


class Security(Base):
    __tablename__ = "securities"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, unique=True, nullable=False, index=True)
    name = Column(String)
    asset_type = Column(String)
    sector = Column(String)
    industry = Column(String)
    exchange = Column(String)
    currency = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    ohlcv_rows = relationship("OHLCV", back_populates="security")
    fundamental_rows = relationship("Fundamental", back_populates="security")


class OHLCV(Base):
    __tablename__ = "ohlcv"
    __table_args__ = (UniqueConstraint("security_id", "date", name="uq_ohlcv_security_date"),)

    id = Column(Integer, primary_key=True)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(Integer)

    security = relationship("Security", back_populates="ohlcv_rows")


class Fundamental(Base):
    __tablename__ = "fundamentals"
    __table_args__ = (
        UniqueConstraint("security_id", "period_end_date", name="uq_fundamentals_security_period"),
    )

    id = Column(Integer, primary_key=True)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=False, index=True)
    period_end_date = Column(Date, nullable=False)
    pe_ratio = Column(Float)
    dividend_yield = Column(Float)
    eps = Column(Float)
    profit = Column(Float)
    revenue = Column(Float)
    market_cap = Column(Float)

    security = relationship("Security", back_populates="fundamental_rows")


class MacroIndicator(Base):
    __tablename__ = "macro_indicators"
    __table_args__ = (
        UniqueConstraint("indicator_code", "date", name="uq_macro_indicator_date"),
    )

    id = Column(Integer, primary_key=True)
    indicator_code = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False)
    value = Column(Float)


class IngestionLog(Base):
    __tablename__ = "ingestion_log"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    target_table = Column(String, nullable=False)
    ref = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, nullable=False)
    rows_ingested = Column(Integer, default=0)
    error_message = Column(String)
    run_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
