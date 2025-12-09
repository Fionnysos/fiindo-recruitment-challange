from src.load_ticker_stats import (
    calc_revenue_growth,
    calc_debt_ratio,
    calc_ttm
)

def test_revenue_growth():
    # basic revenue growth cases
    assert calc_revenue_growth(200, 100) == 1.0
    assert calc_revenue_growth(150, 100) == 0.5

    # invalid inputs return None
    assert calc_revenue_growth(100, 0) is None
    assert calc_revenue_growth(None, 100) is None

def test_debt_ratio():
    # normal calculations
    assert calc_debt_ratio(200, 100) == 2.0
    assert calc_debt_ratio(0, 100) == 0.0

    # invalid inputs return None
    assert calc_debt_ratio(100, 0) is None
    assert calc_debt_ratio(None, 200) is None

def test_ttm():
    # normal valid TTM
    assert calc_ttm([10, 20, 30, 40]) == 100

    # TTM only valid with 4 non-null values
    assert calc_ttm([10, None, 30, 40]) is None
    assert calc_ttm([10, 20]) is None
