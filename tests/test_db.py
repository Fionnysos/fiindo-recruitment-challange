

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.models import Symbol, TickerStatistic, IndustryAggregate


def setup_test_db():
    # create in-memory DB for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionTest = sessionmaker(bind=engine)
    return engine, SessionTest


def test_tables_exist():
    # check if all tables were created
    engine, _ = setup_test_db()
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "symbols" in tables
    assert "ticker_statistics" in tables
    assert "industry_aggregates" in tables


def test_insert_symbol():
    # insert and load a symbol
    _, SessionTest = setup_test_db()
    session = SessionTest()

    sym = Symbol(
        symbol="TEST.US",
        code="TEST",
        exchange="US",
        sector="Technology",
        industry="Software - Application",
    )

    session.add(sym)
    session.commit()

    loaded = session.query(Symbol).filter_by(symbol="TEST.US").first()
    assert loaded is not None
    assert loaded.symbol == "TEST.US"

    session.close()


def test_insert_ticker_stat():
    # insert a ticker stat linked to a symbol
    _, SessionTest = setup_test_db()
    session = SessionTest()

    sym = Symbol(symbol="AAA.US")
    session.add(sym)
    session.commit()

    stat = TickerStatistic(
        symbol_id=sym.id,
        pe_ratio=15.0,
        revenue_growth=0.2,
        net_income_ttm=1000.0,
        debt_ratio=0.5,
        revenue_last_quarter=200.0,
    )

    session.add(stat)
    session.commit()

    loaded = session.query(TickerStatistic).filter_by(symbol_id=sym.id).first()
    assert loaded is not None
    assert loaded.pe_ratio == 15.0

    session.close()
