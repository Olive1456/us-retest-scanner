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

df["SMA30"] = df["Close"].rolling(30).mean()
df["SMA50"] = df["Close"].rolling(50).mean()
df["SMA200"] = df["Close"].rolling(200).mean()

print(df.tail(10)[["Close", "SMA30", "SMA50", "SMA200", "Volume"]])
