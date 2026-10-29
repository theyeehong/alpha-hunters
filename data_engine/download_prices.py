from pathlib import Path
import yfinance as yf
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*inplace.*")


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data" / "raw"


def download_prices(ticker: str, start: str, end: str):
    """Download daily stock prices"""
    prices = yf.download(
        ticker,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        multi_level_index=False,
        progress=False
    )

    if prices is None or prices.empty:
        raise ValueError(f"No data returned for {ticker}")

    prices = prices.sort_index()

    if prices.index.has_duplicates:
        raise ValueError(f"Duplicate dates found for {ticker}")

    required_columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]

    missing_columns = set(required_columns) - set(prices.columns)
    if missing_columns:
        raise ValueError(f"Missing columns {missing_columns} for {ticker}")
    if prices[required_columns].isna().any().any():
        raise ValueError(f"Missing values found for {ticker}")
    if (prices[["Close", "Adj Close"]] < 0).any().any():
        raise ValueError(f"Negative prices found for {ticker}")

    return prices


# def main():
    # ticker = "AAPL"
    # start = "2015-01-01"
    # end = "2026-01-01"

    # prices = download_prices(ticker, start, end)

    # DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    # output_path = DATA_FOLDER / f"{ticker}_{start}_{end}.parquet"
    # prices.to_parquet(output_path)

    # print(f"Downloaded {len(prices):,} rows for {ticker}")
    # print(f"First date: {prices.index.min().date()}")
    # print(f"Last date: {prices.index.max().date()}")
    # print("\nFirst five rows:")
    # print(prices.head(5))
    # print(f"\nData saved to {output_path}")


def main():
    research_tickers = ["AAPL", "MSFT", "GOOGL", "JPM", "XOM"]
    benchmark_ticker = "SPY"
    start = "2015-01-01"
    end = "2026-01-01"

    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    failed_tickers = []

    for ticker in research_tickers + [benchmark_ticker]:
        print(f"Downloading prices for {ticker}...")

        try:
            prices = download_prices(ticker, start, end)
            output_path = DATA_FOLDER / f"{ticker}_{start}_{end}.parquet"
            prices.to_parquet(output_path)

            print(f"Downloaded {len(prices):,} rows for {ticker}")
            print(f"First date: {prices.index.min().date()}")
            print(f"Last date: {prices.index.max().date()}")

        except Exception as e:
            failed_tickers.append(ticker)
            print(f"Failed: {ticker}: {e}")

    if failed_tickers:
        raise RuntimeError(f"Download incomplete. Failed tickers: {failed_tickers}")

    print("\nDownload complete. All tickers downloaded successfully.")


if __name__ == "__main__":
    main()