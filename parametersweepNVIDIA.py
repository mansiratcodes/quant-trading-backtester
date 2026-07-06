import yfinance as yf
import pandas as pd

print("--- Step 4: Optimizing Bot Speed for NVIDIA (NVDA) ---")

# 1. Download NVIDIA data
ticker = "NVDA"
data = yf.download(ticker, start="2025-01-01", end="2026-06-01")

# Clean multi-index columns if they exist
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# 2. Calculate daily market percentage changes
data['Market_Return'] = data['Close'].pct_change()
total_market_growth = (1 + data['Market_Return'].dropna()).prod()
market_final_profit = (total_market_growth - 1) * 100

# 3. Create a loop to test different bot speeds (windows) from 5 days to 50 days
results = []

for window in range(5, 55, 5):
    # Calculate moving average for this specific speed
    mean_col = data['Close'].rolling(window=window).mean()
    
    # Generate signals (1 for buy/hold, 0 for cash)
    signal = (data['Close'] > mean_col).astype(int)
    
    # Calculate daily strategy returns
    strategy_return = data['Market_Return'] * signal.shift(1)
    
    # Compound the daily returns to get the final total profit
    total_strategy_growth = (1 + strategy_return.dropna()).prod()
    strategy_profit = (total_strategy_growth - 1) * 100
    
    # Store the results
    results.append({
        'window': window,
        'profit': strategy_profit
    })

# 4. Print out the leaderboard
print("\n==================================================")
print(f"     SPEED OPTIMIZATION LEADERBOARD FOR {ticker}  ")
print("==================================================")
print(f"Strategy 1: Just BUY & HOLD Nvidia: {market_final_profit:.2f}% Return")
print("--------------------------------------------------")
print("Strategy 2: Your Bot at different speeds:")

# Sort results so the highest profit is at the top
sorted_results = sorted(results, key=lambda x: x['profit'], reverse=True)

for index, res in enumerate(sorted_results):
    prefix = "🏆 BEST -> " if index == 0 else "          "
    print(f"{prefix}{res['window']}-Day Bot: {res['profit']:.2f}% Return")
print("==================================================")