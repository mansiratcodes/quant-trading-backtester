import yfinance as yf
import pandas as pd

print("--- Step 1: Calculating Daily Returns ---")

# 1. Download Apple data
ticker = "AAPL"
data = yf.download(ticker, start="2025-01-01", end="2026-06-01")

# Clean the multi-index columns immediately if they exist
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# 2. Calculate the baseline 20-day moving average
data['20_Day_Mean'] = data['Close'].rolling(window=20).mean()

# 3. Create our Buy (1) or Hold (0) signal based on our rule
# Since the columns are clean, we can compare them directly!
data['Signal'] = 0
data.loc[data['Close'] > data['20_Day_Mean'], 'Signal'] = 1

# 4. MATH: Calculate daily price changes (e.g., 0.02 = +2%, -0.01 = -1%)
data['Market_Return'] = data['Close'].pct_change()

# Print the last 5 days to inspect the raw percentages
print("\n--- Last 5 days of Market Data ---")
print(data[['Close', 'Signal', 'Market_Return']].tail())