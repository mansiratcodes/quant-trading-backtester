import yfinance as yf
import pandas as pd

print("--- Step 2: Calculating Strategy Returns ---")

# 1. Download Apple data
ticker = "AAPL"
data = yf.download(ticker, start="2025-01-01", end="2026-06-01")

# Clean the multi-index columns immediately if they exist
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# 2. Calculate the baseline 20-day moving average
data['20_Day_Mean'] = data['Close'].rolling(window=20).mean()

# 3. Create our Buy (1) or Hold (0) signal based on our rule
data['Signal'] = 0
data.loc[data['Close'] > data['20_Day_Mean'], 'Signal'] = 1

# 4. Calculate daily market price changes
data['Market_Return'] = data['Close'].pct_change()

# 5. NEW STEP: Calculate YOUR Strategy's daily return
# .shift(1) moves the signals down by one day so we use yesterday's decision for today
data['Strategy_Return'] = data['Market_Return'] * data['Signal'].shift(1)

# Print the last 5 days to inspect our progress
print("\n--- Last 5 days of Market & Strategy Returns ---")
print(data[['Close', 'Signal', 'Market_Return', 'Strategy_Return']].tail())
