from .database import engine, Base
from .models import Symbol, TickerStatistic, IndustryAggregate



def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("DB & Tabellen erstellt.")
