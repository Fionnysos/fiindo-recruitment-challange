from database import SessionLocal
from models import Symbol, TickerStatistic, IndustryAggregate
from sqlalchemy import func

# industries we need to aggregate
TARGET_INDUSTRIES = [
    "Banks - Diversified",
    "Software - Application",
]


def main():
    session = SessionLocal()

    # clear old aggregates
    session.query(IndustryAggregate).delete()

    # handle the two exact industries
    for industry in TARGET_INDUSTRIES:
        print(f"calculating aggregates for: {industry}")

        row = (
            session.query(
                func.avg(TickerStatistic.pe_ratio),
                func.avg(TickerStatistic.revenue_growth),
                func.sum(TickerStatistic.revenue_last_quarter)
            )
            .join(Symbol, Symbol.id == TickerStatistic.symbol_id)
            .filter(Symbol.industry == industry)
            .first()
        )

        avg_pe, avg_growth, sum_revenue = row

        session.add(IndustryAggregate(
            industry=industry,
            avg_pe_ratio=avg_pe,
            avg_revenue_growth=avg_growth,
            sum_revenue=sum_revenue
        ))

    # handle Consumer Cyclical via sector
    print("calculating aggregates for: Consumer Cyclical")

    row = (
        session.query(
            func.avg(TickerStatistic.pe_ratio),
            func.avg(TickerStatistic.revenue_growth),
            func.sum(TickerStatistic.revenue_last_quarter)
        )
        .join(Symbol, Symbol.id == TickerStatistic.symbol_id)
        .filter(Symbol.sector == "Consumer Cyclical")
        .first()
    )

    avg_pe, avg_growth, sum_revenue = row

    session.add(IndustryAggregate(
        industry="Consumer Cyclical",
        avg_pe_ratio=avg_pe,
        avg_revenue_growth=avg_growth,
        sum_revenue=sum_revenue
    ))

    session.commit()
    session.close()
    print("industry aggregates saved")


if __name__ == "__main__":
    main()
