import pandas as pd
import pytest
from data_engine.calculate_returns import calculate_returns


def test_daily_returns_match_known_values():
    prices = pd.DataFrame(
        {"Adj Close": [100.0, 110.0, 99.0]},
        index=pd.to_datetime(["2030-01-01", "2030-01-02", "2030-01-03"]),
    )

    result = calculate_returns(prices)

    assert pd.isna(result["daily_return"].iloc[0])

    assert result["daily_return"].iloc[1] == pytest.approx(0.10)
    assert result["daily_return"].iloc[2] == pytest.approx(-0.10)

    compounded_return = (1 + result["daily_return"].dropna()).prod()
    assert compounded_return == pytest.approx(99.0/100.0)


def test_missing_prices_are_rejected():
    prices = pd.DataFrame(
        {"Adj Close": [100.0, float("nan"), 99.0]},
        index=pd.to_datetime(["2030-01-01", "2030-01-02", "2030-01-03"]),
    )

    with pytest.raises(ValueError): 
        calculate_returns(prices)


def test_duplicate_dates_are_rejected():
    prices = pd.DataFrame(
        {"Adj Close": [100.0, 110.0, 99.0]},
        index=pd.to_datetime(["2030-01-01", "2030-01-01", "2030-01-03"]),
    )

    with pytest.raises(ValueError): 
        calculate_returns(prices)