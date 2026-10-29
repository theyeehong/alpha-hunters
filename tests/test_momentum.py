import pandas as pd
import pytest

from alpha_hunting.momentum.cross_sectional_momentum import (
    calculate_momentum,
)


def example_prices():
    return pd.DataFrame(
        {"TEST": [100.0] + [110.0] * 10 + [120.0, 999.0]},
        index=pd.date_range("2024-01-31", periods=13, freq="ME"),
    )


def test_momentum_matches_known_value():
    scores = calculate_momentum(example_prices())

    # At January 2025: December 2024 / January 2024 - 1.
    assert scores.loc["2025-01-31", "TEST"] == pytest.approx(0.20)

    # Earlier rows lack the required history.
    assert scores.iloc[:12]["TEST"].isna().all()


def test_latest_month_is_excluded():
    prices = example_prices()
    original = calculate_momentum(prices)

    # Changing January 2025 must not affect its momentum score.
    prices.loc["2025-01-31", "TEST"] = 1.0
    changed = calculate_momentum(prices)

    assert changed.loc["2025-01-31", "TEST"] == pytest.approx(
        original.loc["2025-01-31", "TEST"]
    )