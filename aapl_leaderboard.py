import yfinance as yf
import pandas as pd

print("--- Step 3: Running the Final Scorecard Simulation ---")

# 1. Download Apple data (From Jan 2025 to June 2026)
ticker = "AAPL"
data = yf.download(ticker, start="2025-01-01", end="2026-06-01")

# Clean up column layers immediately
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# 2. Calculate the baseline 20-day normal average
data['20_Day_Mean'] = data['Close'].rolling(window=20).mean()

# 3. Create the Buy (1) or Hold (0) signals
data['Signal'] = 0
data.loc[data['Close'] > data['20_Day_Mean'], 'Signal'] = 1

# 4. Calculate the daily market percentage changes
data['Market_Return'] = data['Close'].pct_change()

# 5. Calculate your Bot's daily strategy returns (using yesterday's signal)
data['Strategy_Return'] = data['Market_Return'] * data['Signal'].shift(1)

# 6. MATH STEP: Multiply all daily returns together to get the grand total growth
# .dropna() just cleans out any empty rows at the very beginning
total_market_growth = (1 + data['Market_Return'].dropna()).prod()
total_strategy_growth = (1 + data['Strategy_Return'].dropna()).prod()

# 7. Convert the growth factors into clean, readable percentages
market_final_profit = (total_market_growth - 1) * 100
strategy_final_profit = (total_strategy_growth - 1) * 100

# 8. Print out the final scorecard
print("\n==================================================")
print(f"      FINAL BACKTEST RESULTS FOR {ticker}         ")
print("==================================================")
print(f"Strategy 1: If you just BOUGHT & HELD Apple stock:")
print(f"--> Total Profit: {market_final_profit:.2f}%")
print("\nStrategy 2: If you followed YOUR Robot's Signals:")
print(f"--> Total Profit: {strategy_final_profit:.2f}%")
print("==================================================")
