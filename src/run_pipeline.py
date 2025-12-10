# runs the full ETL pipeline

import time

from .init_db import init_db
from .load_symbols import main as load_symbols
from .load_ticker_stats import main as load_stats
from .load_industry_aggregates import main as load_aggregates


def main():
    print("init db...")
    init_db()
    time.sleep(0.5)

    print("load symbols...")
    load_symbols()
    time.sleep(0.5)

    print("load ticker stats...")
    load_stats()
    time.sleep(0.5)

    print("load industry aggregates...")
    load_aggregates()

    print("pipeline done")


if __name__ == "__main__":
    main()
