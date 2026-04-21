import numpy as np
import pandas as pd
import mplfinance as mpf

def generate_stock_data(start_price, end_price, deviation_score, duration):
    prices = [start_price]
    volumes = []
    
    drift = 0.05 * (0.5 + deviation_score) 
    
    for i in range(duration):
        current_price = prices[-1]

        daily_drift = (end_price - current_price) / (duration - i )
        
        direction_weight = np.random.rand()
        direction = 1 if direction_weight > 0.5 else -1
        
        move_strength = np.random.normal(0, deviation_score*0.25)
        
        noise = np.random.normal(0, deviation_score) 
        
        next_price = current_price + drift + daily_drift + direction * move_strength * current_price + noise
        
        upper_bound = max(start_price, end_price) * 1.5
        lower_bound = min(start_price, end_price) * 0.5
        
        next_price = np.clip(next_price, lower_bound, upper_bound)
        
        prices.append(max(0.1, next_price))
    
    data = []
    
    for i in range(duration):
        open_price = prices[i]
        close_price = prices[i + 1]
        
        candle_size = abs(close_price - open_price)
        
        wick_factor = np.random.uniform(0.1, 0.6)
        
        high_price = max(open_price, close_price) * (1 + wick_factor * 0.01)
        low_price = min(open_price, close_price) * (1 - wick_factor * 0.01)
        
        volume = int(np.random.randint(1000, 10000) * (1 + candle_size / open_price))
        
        data.append([open_price, close_price, high_price, low_price, volume])
    
    return pd.DataFrame(data, columns=["open","close","high","low","volume"])

def plot_tradingview_style(df):
    df = df.copy()
    
    df['Date'] = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
    df.set_index('Date', inplace=True)
    
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)
    
    style = mpf.make_mpf_style(
        base_mpf_style='nightclouds',
        rc={'font.size': 8}
    )
    
    mpf.plot(
    df,
    type="candle",
    volume=True,
    style="yahoo",
    title="Synthetic Stock Data",
    mav=(20,50,200),
    figsize=(12,7)
)

if __name__ == "__main__":
    df = generate_stock_data(
        start_price=20,
        end_price=1360,
        deviation_score=0.15,
        duration=5750
    )#5750
    df.to_csv("synthetic_stock_data.csv", index=False)
    plot_tradingview_style(df)