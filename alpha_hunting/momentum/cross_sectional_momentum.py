from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"


def calculate_momentum(adjusted_price: pd.DataFrame):
    """calculate month end momentum, excluding latest month"""
    if adjusted_price.empty:
        raise ValueError("The price table is empty.")

    if not isinstance(adjusted_price.index, pd.DatetimeIndex):
        raise ValueError("Prices must have a datetime index.")

    if adjusted_price.index.has_duplicates:
        raise ValueError("Prices must have a unique datetime index.")

    if adjusted_price.isna().any().any():
        raise ValueError("Missing price values found.")

    if (adjusted_price <= 0).any().any():
        raise ValueError("Prices must be positive.")

    adjusted_price = adjusted_price.sort_index()

    monthly_prices = adjusted_price.resample("ME").last()
    momentum = monthly_prices.shift(1) / monthly_prices.shift(12) - 1

    return momentum


def main():
    input_path = PROCESSED_FOLDER / "adjusted_prices.parquet"

    if not input_path.exists():
        raise FileNotFoundError(f"Price file not found: {input_path}")

    prices = pd.read_parquet(input_path)

    research_tickers = ["AAPL", "MSFT", "GOOGL", "JPM", "XOM"]
    momentum = calculate_momentum(prices[research_tickers])

    eligible_scores = momentum.dropna(how="any")

    if eligible_scores.empty:
        raise ValueError("Not enough history to rank all stocks")

    output_path = PROCESSED_FOLDER / "momentum_scores.parquet"
    momentum.to_parquet(output_path)

    latest_date = eligible_scores.index[-1]
    latest_rankings = eligible_scores.loc[latest_date].sort_values(ascending=False)

    print(f"\nMomentum ranking for {latest_date.date()}:")
    print(latest_rankings.rename("momentum").to_frame())
    print(f"\nMomentum scores saved to {output_path}")


if __name__ == "__main__":
    main()