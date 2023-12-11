import pandas as pd
from binance.spot import Spot
import mplfinance as mpf
import matplotlib.pyplot as plt

binance_client = Spot()

from backtest_functions import get_data

symbol = "SOLUSDT"
interval = '15m'
limit = '1000' # 1k candles back

qty = 1  # place 1 contract per order
step_size_down = 0.7
step_size_up = 0.7 # place limit orders every 0.5 dollar of price change
max_entry_size = 5 # maximum entry size in contracts

buy_limit_orders = []
sell_limit_orders = []



current_position_orders = []

bought_orders = []
sold_orders = []

frame = get_data(binance_client, symbol, interval, limit)

# write a function that will create the buy and sell limit orders at the opening price of the candle based on the current position orders and the max entry size
def place_limit_orders(candle: pd.DataFrame, step_size_up: float, step_size_down: float, max_entry_size: int, current_position_orders: list, qty: float):
    
    buy_limit_orders = []
    sell_limit_orders = []
    
    if len(current_position_orders) == 0:
        print(f"set {max_entry_size} limit buy orders bellow the price in steps of {step_size_down} dollar")
    
        for i in range(1, max_entry_size + 1):
            buy_limit_orders.append(candle['Open'] - i * step_size_down)
        
        # print(f"buy orders: {buy_limit_orders}")
        
        sell_limit_orders = []
        
    elif len(current_position_orders) == max_entry_size:
        print(f"set {max_entry_size} limit sell orders above the price in steps of {step_size_up} dollar")
    
        for i in range(1, max_entry_size + 1):
            sell_limit_orders.append(candle['Open'] + i * step_size_up)
        
        # print(f"sell orders: {sell_limit_orders}")
        buy_limit_orders = []
    
    elif len(current_position_orders) > 0 and len(current_position_orders) < max_entry_size:
        position_size_left = max_entry_size - len(current_position_orders)
        print(f"set {position_size_left} limit buy orders bellow the price in steps of {step_size_down} dollar")
    
        for i in range(1, int(position_size_left) + 1):
            buy_limit_orders.append(candle['Open'] - i * step_size_down)
        
        # print(f"buy orders: {buy_limit_orders}")
        
        print(f"set {len(current_position_orders)} limit sell orders above the price in steps of {step_size_up} dollar")
    
        for i in range(1, len(current_position_orders) + 1):
            sell_limit_orders.append(candle['Open'] + i * step_size_up)
        
        # print(f"sell orders: {sell_limit_orders}")
    
    return buy_limit_orders, sell_limit_orders

# write a function that will check if the limit orders have been filled
def check_if_orders_filled(buy_limit_orders: list, sell_limit_orders: list, candle: pd.DataFrame, current_position_orders: list,  qty: float, bought_orders: list, sold_orders: list):
    
    # check if the buy limit orders have been filled
    if len(buy_limit_orders) > 0:
        for i in range(len(buy_limit_orders)):
            if candle['Low'] <= buy_limit_orders[i]:
                print(f"buy limit order {buy_limit_orders[i]} has been filled")
                current_position_orders.append(buy_limit_orders[i])
                bought_orders.append(buy_limit_orders[i])
                buy_limit_orders.pop(i)
                break
    
    # check if the sell limit orders have been filled
    if len(sell_limit_orders) > 0:
        for i in range(len(sell_limit_orders)):
            if candle['High'] >= sell_limit_orders[i]:
                print(f"sell limit order {sell_limit_orders[i]} has been filled")
                current_position_orders.pop(i)
                sold_orders.append(sell_limit_orders[i])
                sell_limit_orders.pop(i)
                break
    
    else:
        print("no limit orders have been filled for the current candlestick")
    
    return current_position_orders, sold_orders, bought_orders



# get the first 3 candles
candles = frame
# print(candles)

for index, row in candles.iterrows():
    
    print(row)
    
    buy_limit_orders, sell_limit_orders = place_limit_orders(row, step_size_up, step_size_down, max_entry_size, current_position_orders, qty)

    # print ("__________________________________________________________\n")
    print("BUY ORDERS")
    print(buy_limit_orders)

    print("SELL ORDERS")
    print(sell_limit_orders)
    print ("__________________________________________________________\n")
    
    current_position_orders, sold_orders, bought_orders = check_if_orders_filled(buy_limit_orders, sell_limit_orders, row, current_position_orders, qty, bought_orders, sold_orders)
    
    print ("__________________________________________________________\n")
    print("CURRENT POSITION ORDERS")
    print(current_position_orders)
    
    print("SOLD ORDERS")
    print(sold_orders)
    
    print("BOUGHT ORDERS")
    print(bought_orders)
    print ("__________________________________________________________\n")


# write a function that will calculate pnl between bought and sold orders

def calculate_pnl(bought_orders: list, sold_orders: list, current_position_orders: list):
    
    pnl = 0
    
    # make sure the lists are of the same length
    if len(bought_orders) == len(sold_orders):
        for i in range(len(bought_orders)):
            
            trade_pnl = round(sold_orders[i] - bought_orders[i], 2)
            print(f"trade pnl: {trade_pnl}")
            pnl += trade_pnl
    
    else:
        # remove the last elements from bought orders
        bought_orders = bought_orders[:len(sold_orders)]
        for i in range(len(bought_orders)):
            trade_pnl = round(sold_orders[i] - bought_orders[i], 2)
            print(f"trade pnl: {trade_pnl}")
            pnl += trade_pnl

    return round(pnl, 2)

pnl = calculate_pnl(bought_orders, sold_orders, current_position_orders)

print(f"pnl: {pnl}")



mpf.plot(frame, type='candle', style='yahoo', volume=False, figsize=(16,9), tight_layout=True, xrotation=0, datetime_format='%d-%m-%Y %H:%M:%S', ylabel='Price (USDT)')
mpf.show()