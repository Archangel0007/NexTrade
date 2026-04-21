import numpy as np
import pandas as pd
import mplfinance as mpf

def generate_path_between_prices(
    start_price=100,
    end_price=150,
    days=200,
    volatility=0.02,
    seed=42
):
    np.random.seed(seed)

    # required drift so final price hits target
    drift = np.log(end_price/start_price) / days

    prices = [start_price]

    for _ in range(days):
        shock = np.random.normal(drift, volatility)
        price = prices[-1] * np.exp(shock)
        prices.append(price)

    prices = np.array(prices)

    # adjust final value exactly
    adjustment_factor = end_price / prices[-1]
    prices = prices * adjustment_factor

    df = pd.DataFrame({
        "Close": prices[1:]
    })

    # OHLC construction
    df["Open"] = df["Close"].shift(1)
    df.loc[0,"Open"] = start_price

    noise = np.random.uniform(0.002,0.02,len(df))

    df["High"] = df[["Open","Close"]].max(axis=1) * (1 + noise)
    df["Low"] = df[["Open","Close"]].min(axis=1) * (1 - noise)

    returns = df["Close"].pct_change().fillna(0)
    df["Volume"] = (1e6*(1+abs(returns)*40)).astype(int)

    df["Date"] = pd.date_range("2022-01-01", periods=len(df))
    df.set_index("Date", inplace=True)

    return df


df = generate_path_between_prices(
    start_price=100,
    end_price=180,
    days=250,
    volatility=0.025
)

# plot
mpf.plot(
    df,
    type="candle",
    volume=True,
    style="yahoo",
    mav=(20,50),
    title="Controlled Start-End Synthetic Stock"
)

print(df.tail())