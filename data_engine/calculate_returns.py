from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"


def calculate_returns(prices: pd.DataFrame):
    """Calculate daily returns from adjusted stock prices"""
    if prices.empty:
        raise ValueError("The price dataset is empty")

    if "Adj Close" not in prices.columns:
        raise ValueError("The dataset must contain 'Adj Close'")

    if prices.index.has_duplicates:
        raise ValueError("Duplicate dates found")

    prices = prices.sort_index()
    adjusted_close = prices["Adj Close"]

    if adjusted_close.isna().any():
        raise ValueError("Missing values found in 'Adj Close'")

    if (adjusted_close < 0).any():
        raise ValueError("Negative prices found in 'Adj Close'")

    result = pd.DataFrame(index=prices.index)
    result["adjusted_close"] = adjusted_close
    result["daily_return"] = adjusted_close.pct_change(fill_method=None)

    return result


# def main():
    # filename = "AAPL_2015-01-01_2026-01-01.parquet"
    # input_path = RAW_FOLDER / filename

    # if not input_path.exists():
    #     raise FileNotFoundError(f"Input file {input_path} does not exist")

    # prices = pd.read_parquet(input_path)
    # returns = calculate_returns(prices)

    # PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)
    # output_path = PROCESSED_FOLDER / filename
    # returns.to_parquet(output_path)

    # print(f"\nFirst five rows:")
    # print(returns.head(5))

    # print("\nDaily return summary:")
    # print(returns["daily_return"].describe())

    # print(f"\nData saved to {output_path}")


def main():
    research_tickers = ["AAPL", "MSFT", "GOOGL", "JPM", "XOM"]
    benchmark_ticker = "SPY"
    start = "2015-01-01"
    end = "2026-01-01"
    tickers = research_tickers + [benchmark_ticker]

    adjusted_prices = {}
    daily_returns = {}

    for ticker in tickers:
        input_path = RAW_FOLDER / f"{ticker}_{start}_{end}.parquet"

        if not input_path.exists():
            raise FileNotFoundError(f"Input file {input_path} does not exist")

        prices = pd.read_parquet(input_path)
        returns = calculate_returns(prices)

        adjusted_prices[ticker] = returns["adjusted_close"]
        daily_returns[ticker] = returns["daily_return"]

        print(f"Processed {ticker}: {len(returns):,} rows")

    prices_table = pd.concat(adjusted_prices, axis=1).sort_index()
    returns_table = pd.concat(daily_returns, axis=1).sort_index()

    prices_table.index.name = "Date"
    returns_table.index.name = "Date"

    PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)
    prices_path = PROCESSED_FOLDER / f"adjusted_prices.parquet"
    returns_path = PROCESSED_FOLDER / f"daily_returns.parquet"

    prices_table.to_parquet(prices_path)
    returns_table.to_parquet(returns_path)

    print("\nFirst five rows of adjusted prices:")
    print(prices_table.head(5))

    print("\nFirst five rows of daily returns:")
    print(returns_table.head(5))

    print("\nMissing adjusted prices per ticker:")
    print(prices_table.isnull().sum())

    print("\nMissing daily returns per ticker:")
    print(returns_table.isnull().sum())

    print(f"\nAdjusted prices saved to {prices_path}")
    print(f"Daily returns saved to {returns_path}")


if __name__ == "__main__":
    main()