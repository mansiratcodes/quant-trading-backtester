# Quantitative Trading Backtesting & Optimization Engine 📈

Welcome to my quantitative development portfolio. This repository contains a modular Python framework built to pull live historical equity data, backtest trend-following strategies, and run automated parameter optimization sweeps against high-volatility assets.

## 🗂️ Repository Structure & Files

*   `50dayavg.py` / `Nvidia50day.py`: Core logic engines evaluating 50-day moving average baselines.
*   `marketreturn.py` / `strategyreturn.py`: Vectorized pipeline components isolating base market performance from strategy execution.
*   `parametersweepNVIDIA.py` / `finale.py`: Automated optimization scripts designed to stress-test indicators across multiple time windows.

---

## 🛠️ Core Architectural Highlights

*   **Vectorized Execution:** Uses native `pandas` lookups instead of slow iterative loops to simulate years of historical data instantly.
*   **Look-Ahead Bias Protection:** Implements a `.shift(1)` execution delay on trading signals, ensuring the bot never "cheats" by using future data points.
*   **Data Normalization:** Automatically flattens multi-index data structures returned by the modern `yfinance` API to prevent runtime crashes.

---

## 📊 Empirical Simulation Results

### 1. Steady Trend Tracking (Apple - AAPL)
Using a patient, heavy 50-day moving average anchor, the system filtered out short-term market noise and successfully bypassed minor dips.
*   **Benchmark Return (Buy & Hold):** 28.79%
*   **Algorithmic Bot Return:** **37.92%**
*   **Net Alpha:** **+9.13% outperformance**

### 2. High-Volatility Parameter Optimization (NVIDIA - NVDA)
When applied to a hyper-volatile momentum asset, a standard 50-day window proved too slow, lagging behind major trend shifts. By executing a brute-force parameter sweep across windows from 5 to 50 days, the script automatically identified a hidden mathematical "sweet spot."
*   **Benchmark Return (Buy & Hold):** 52.71%
*   **The 50-Day Bot Return:** 42.37% (Lagged the market)
*   **Optimized 45-Day Bot Return:** **60.94%** 🏆
*   **Net Alpha:** **+8.23% outperformance over the market**

---

## 🚀 Technical Requirements
*   Python 3.x
*   `pandas`
*   `yfinance`
