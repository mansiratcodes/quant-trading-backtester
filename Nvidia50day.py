import yfinance as yf
import pandas as pd

print("--- Step 3 (NVIDIA Test): Running 50-Day Simulation on NVDA ---")

# 1. NEW TICKER: We changed "AAPL" to "NVDA"
ticker = "NVDA"
data = yf.download(ticker, start="2025-01-01", end="2026-06-01")

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# 2. Calculate the 50-day moving average
data['50_Day_Mean'] = data['Close'].rolling(window=50).mean()

# 3. Create signals
data['Signal'] = 0
data.loc[data['Close'] > data['50_Day_Mean'], 'Signal'] = 1

# 4. Calculate daily market percentage changes
data['Market_Return'] = data['Close'].pct_change()

# 5. Calculate your Bot's daily strategy returns
data['Strategy_Return'] = data['Market_Return'] * data['Signal'].shift(1)

# 6. Multiply all daily returns together to get total growth
total_market_growth = (1 + data['Market_Return'].dropna()).prod()
total_strategy_growth = (1 + data['Strategy_Return'].dropna()).prod()

# 7. Convert to clean percentages
market_final_profit = (total_market_growth - 1) * 100
strategy_final_profit = (total_strategy_growth - 1) * 100

# 8. Print out the final scorecard
print("\n==================================================")
print(f"      FINAL 50-DAY RESULTS FOR {ticker}         ")
print("==================================================")
print(f"Strategy 1: If you just BOUGHT & HELD Nvidia stock:")
print(f"--> Total Profit: {market_final_profit:.2f}%")
print("\nStrategy 2: If you followed YOUR 50-Day Robot:")
print(f"--> Total Profit: {strategy_final_profit:.2f}%")
print("==================================================")