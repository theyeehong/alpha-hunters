# Experiment 001: Cross-sectional MOMENTUM

## Research question
Do stocks with higher past returns outperforms stocks with weaker past returns over the following month?

## Hypothesis
Stocks ranked higher by past returns may continue outperforming lower ranked stocks.
Will test if it survives trading costs and evaluation on unseen data

## Initial scope
- US equities
- Daily price data
- Monthly signal calculation and portfolio rebalancing
- Long only portfolio
- No leverage

## Signal
At each month end:
1. Measure each stock's return from 12 months earlier to 1 month earlier
2. Exclude the most recent month's return
3. Rank eligible ones from strongest to weakest
Only information available at the signal date will be used

## Portfolio rule
- Hold the highest ranked 20pct of eligible stocks
- Give selected stocks equal target weights
- Trade after the signal becomes available
- Model transactions cost explicitly

## Comparisons
- An equally weighted portfolio of the same eligible stock universe
- A broad US equity market benchmark

## Evaluation
Record:
- Annualized return and volatility
- Sharpe ratio
- Maximum drawdown
- Portfolio turnover
- Performance before and after trading costs
Choose and record the research and holdout periods before evaluating strategy performance. Do not tune the strategy using the final holdout

## Data requirements
- Consistent trading dates and stock identifiers
- Document treatment of splits and dividends
- Missing data and duplicate checks
- Sufficient history to calculate the signal
- Document universe membership and delisting coverage
(A universe chosen from stocks surviving today introduces suvivorship bias. Any such limitation must appear in the conclusions)

## Status
Hypothesis defined
Data preparation starting
