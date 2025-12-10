""" Database models for the Fiindo recruitment challenge. """
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, unique=True, nullable=False)
    code = Column(String)
    exchange = Column(String)
    company_name = Column(String)
    sector = Column(String)
    industry = Column(String)
    country = Column(String)
    currency = Column(String)
    market_cap = Column(Float)

    stats = relationship("TickerStatistic", back_populates="symbol_obj")


class TickerStatistic(Base):
    __tablename__ = "ticker_statistics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)

    pe_ratio = Column(Float)
    revenue_growth = Column(Float)
    net_income_ttm = Column(Float)
    debt_ratio = Column(Float)
    revenue_last_quarter = Column(Float)
    calculated_at = Column(String)

    symbol_obj = relationship("Symbol", back_populates="stats")

class IndustryAggregate(Base):
    __tablename__ = "industry_aggregates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry = Column(String, unique=True, nullable=False)

    avg_pe_ratio = Column(Float)
    avg_revenue_growth = Column(Float)
    sum_revenue = Column(Float)
