import yfinance as yf
import pandas as pd

ticker = "AAPL"

df = yf.download(
    ticker,
    period="1y",
    interval="1d",
    auto_adjust=False,
    progress=False
)

weights = pd.Series(range(1, 31), dtype=float)

df["WMA30"] = df["Close"].rolling(30).apply(
    lambda prices: (prices * weights.values).sum() / weights.sum(),
    raw=True
)

df["SMA50"] = df["Close"].rolling(50).mean()
df["SMA200"] = df["Close"].rolling(200).mean()

print(df.tail(10)[["Close", "WMA30", "SMA50", "SMA200", "Volume"]])
