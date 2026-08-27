import yfinance as yf
import pandas as pd

tickers = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "META",
    "TSLA",
    "AMD",
    "ARM",
    "PACB",
    "FE"
]

results = []

weights = pd.Series(range(1, 31), dtype=float)

for ticker in tickers:
    try:
        df = yf.download(
            ticker,
            period="1y",
            interval="1d",
            auto_adjust=False,
            progress=False
        )

        if len(df) < 200:
            continue

        close = df["Close"].squeeze()
        volume = df["Volume"].squeeze()

        wma30 = close.rolling(30).apply(
            lambda prices: (prices * weights.values).sum() / weights.sum(),
            raw=True
        )

        sma50 = close.rolling(50).mean()
        sma200 = close.rolling(200).mean()

        latest = pd.DataFrame({
            "Close": close,
            "WMA30": wma30,
            "SMA50": sma50,
            "SMA200": sma200,
            "Volume": volume
        }).dropna().iloc[-1]

        above_sma200 = latest["Close"] > latest["SMA200"]

        results.append({
            "Ticker": ticker,
            "Close": round(latest["Close"], 2),
            "WMA30": round(latest["WMA30"], 2),
            "SMA50": round(latest["SMA50"], 2),
            "SMA200": round(latest["SMA200"], 2),
            "Volume": int(latest["Volume"]),
            "Above_SMA200": above_sma200
        })

    except Exception as e:
        print(f"Error downloading {ticker}: {e}")

result_df = pd.DataFrame(results)

print("\nALL STOCKS")
print(result_df.to_string(index=False))

print("\nABOVE SMA200")
print(
    result_df[result_df["Above_SMA200"] == True]
    .sort_values("Ticker")
    .to_string(index=False)
)
