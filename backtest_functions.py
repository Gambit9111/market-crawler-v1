import pandas as pd
from binance.spot import Spot

def get_data(binance_client: Spot, symbol: str, interval: str, limit: int) -> pd.DataFrame:
    df = pd.DataFrame(binance_client.klines(symbol=symbol, interval=interval, limit=limit))
    df = df.iloc[:, :9]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_av', 'Trades']

    # drop unnecessary columns
    df = df.drop(['Close_time', 'Quote_av', 'Trades'], axis=1)

    # convert to datetime
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')

    # set index
    df = df.set_index('Time')
    # convert to float
    df = df.astype(float)

    return df