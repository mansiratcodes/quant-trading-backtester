import yfinance as yf
import pandas as pd

def run_crossover_backtest(ticker="AAPL", start_date="2025-01-01", end_date="2026-06-01", fast_w=20, slow_w=50):
    print(f"--- Fetching Data for {ticker} ---")
    data = yf.download(ticker, start=start_date, end=end_date)
    
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    print(f"--- Calculating Dual Indicators: Fast ({fast_w} Days) vs Slow ({slow_w} Days) ---")
    # Compute short-term and long-term moving averages
    data['Fast_SMA'] = data['Close'].rolling(window=fast_w).mean()
    data['Slow_SMA'] = data['Close'].rolling(window=slow_w).mean()
    
    # Generate trading signals
    data['Signal'] = 0
    # Condition: 1 (Long) when short-term momentum is higher than long-term trend
    data.loc[data['Fast_SMA'] > data['Slow_SMA'], 'Signal'] = 1
    
    # Calculate performance pipelines
    data['Market_Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Market_Return'] * data['Signal'].shift(1)
    
    # Compound total returns
    market_profit = ((1 + data['Market_Return'].dropna()).prod() - 1) * 100
    strategy_profit = ((1 + data['Strategy_Return'].dropna()).prod() - 1) * 100
    
    print("\n" + "="*50)
    print(f"      CROSSOVER SCORECARD FOR {ticker}         ")
    print("="*50)
    print(f"Fast Window: {fast_w} Days  |  Slow Window: {slow_w} Days")
    print(f"Benchmark Market Return : {market_profit:.2f}%")
    print(f"Crossover Strategy Return: {strategy_profit:.2f}%")
    print("="*50 + "\n")
    
    return market_profit, strategy_profit

if __name__ == "__main__":
    # Test execution using standard 20/50 dual crossover rules
    run_crossover_backtest(ticker="AAPL", fast_w=20, slow_w=50)