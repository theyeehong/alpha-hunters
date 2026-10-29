from math import ceil
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"


def create_target_weights(scores: pd.DataFrame, top_fraction: float=0.2):
    """Select the strongest stocks and assign equal target weights"""
    if not 0 < top_fraction < 1:
        raise ValueError("top_fraction must be between 0 and 1.")

    if scores.empty:
        raise ValueError("The scores table is empty.")

    if scores.columns.has_duplicates:
        raise ValueError("Duplicate tickers found")

    if not np.isfinite(scores.to_numpy()).all():
        raise ValueError("Scores must be finite numbers.")

    scores = scores.sort_index(axis=1)

    number_to_hold = ceil(len(scores.columns) * top_fraction)

    ranks = scores.rank(axis=1, ascending=False, method="first")

    selected = ranks <= number_to_hold
    weights = selected.astype(float) / number_to_hold

    return weights


def main():
    input_path = PROCESSED_FOLDER / "momentum_scores.parquet"
    scores = pd.read_parquet(input_path)

    eligible_scores = scores.dropna(how="any")

    weights = create_target_weights(eligible_scores, top_fraction=0.2)

    output_path = PROCESSED_FOLDER / "target_weights.parquet"
    weights.to_parquet(output_path)

    print(f"\nTarget weights for {weights.index[-1].date()}:")
    print(weights.iloc[-1].sort_values(ascending=False).map("{:.1%}".format))
    print(f"\nTarget weights saved to {output_path}")


if __name__ == "__main__":
    main()
