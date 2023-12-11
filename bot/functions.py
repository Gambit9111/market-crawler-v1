from pybit.unified_trading import HTTP
from datetime import datetime, timedelta

def ask_bid(session: HTTP, symbol: str) -> tuple:
    """
    _description_
    generate latest ask and bid prices for a given symbol

    Args:
        session (HTTP): bybit http session
        symbol (str): trading pair

    Returns:
        tuple: returns a tuple of ask and bid prices
    """
    
    
    ob = session.get_orderbook(category="linear", symbol=symbol)
    
    ask = float(ob['result']['a'][0][0])
    bid = float(ob['result']['b'][0][0])
    
    # print(f"Ask: {ask}")
    # print(f"Bid: {bid}")
    
    return ask, bid


def open_long_position(session: HTTP, symbol: str, orderType: str, qty: float, price: float) -> None:
    """ open a long position
    Args:
        session (HTTP): _description_
        symbol (str): _description_
        orderType (str): _description_
        qty (float): _description_
        price (float): _description_
    """
    long_position = session.place_order(
        category="linear",
        symbol=symbol,
        side="Buy",
        orderType=orderType,
        qty=qty,
        price=price,
        reduceOnly=False,
    )
    print(f"open long position @ {price}, qty: {qty}")
    # print(long_position)



def close_long_position(session: HTTP, symbol: str, orderType: str, qty: float, price: float) -> None:
    """ close a long position
    Args:
        session (HTTP): _description_
        symbol (str): _description_
        orderType (str): _description_
        qty (float): _description_
        price (float): _description_
    """
    long_position = session.place_order(
        category="linear",
        symbol=symbol,
        side="Sell",
        orderType=orderType,
        qty=qty,
        price=price,
        reduceOnly=True,
    )
    print(f"close long position @ {price}, qty: {qty}")
    # print(long_position)

def cancel_all_orders(session: HTTP, symbol: str) -> None:
    """ cancel all orders
    Args:
        session (HTTP): _description_
        symbol (str): _description_
    """
    session.cancel_all_orders(
        category="linear",
        symbol=symbol,
    )
    print("Successfully cancelled all orders")

def get_current_position(session: HTTP, symbol: str) -> tuple:
    """ get current position information
    Args:
        session (HTTP): _description_
        symbol (str): _description_
        
    Returns:
        current_position_symbol (str): _description_
        current_position_average_entry_price (float): _description_
        current_position_market_price (float): _description_
        current_position_qty (float): _description_
        current_position_side (str): _description_
        current_position_leverage (int): _description_
        current_position_liq_price (float): _description_
        current_position_unrealised_pnl (float): _description_
        current_position_created_time (str): _description_
        current_position_updated_time (str): _description_
    """
    position = session.get_positions(
        category="linear",
        symbol=symbol,
    )
    
    current_position_symbol = position['result']['list'][0]['symbol']
    current_position_average_entry_price = float(position['result']['list'][0]['avgPrice'])
    current_position_market_price = float(position['result']['list'][0]['markPrice'])
    current_position_qty = float(position['result']['list'][0]['size'])
    current_position_side = position['result']['list'][0]['side']
    current_position_leverage = int(position['result']['list'][0]['leverage'])
    current_position_liq_price = position['result']['list'][0]['liqPrice']
    current_position_unrealised_pnl = position['result']['list'][0]['unrealisedPnl']
    # we calculate time in utc-5 (new york time)
    current_position_created_time = (datetime.utcfromtimestamp(int(position['result']['list'][0]['createdTime']) / 1000) - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
    current_position_updated_time = (datetime.utcfromtimestamp(int(position['result']['list'][0]['updatedTime']) / 1000) - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
    
    
    # print(f"Current position symbol: {current_position_symbol}")
    # print(f"Current position average entry price: {current_position_average_entry_price}")
    # print(f"Current position market price: {current_position_market_price}")
    # print(f"Current position qty: {current_position_qty}")
    # print(f"Current position side: {current_position_side}")
    # print(f"Current position leverage: {current_position_leverage}")
    # print(f"Current position liq price: {current_position_liq_price}")
    # print(f"Current position unrealised pnl: {current_position_unrealised_pnl}")
    # print(f"Current position created time: {current_position_created_time}")
    # print(f"Current position updated time: {current_position_updated_time}")
    
    # print(position['result'])
    
    return current_position_symbol, current_position_average_entry_price, current_position_market_price, current_position_qty, current_position_side, current_position_leverage, current_position_liq_price, current_position_unrealised_pnl, current_position_created_time, current_position_updated_time

def set_leverage(session: HTTP, symbol: str, leverage: str) -> None:
    """ set leverage
    Args:
        session (HTTP): _description_
        symbol (str): _description_
        leverage (int): _description_
    """
    session.set_leverage(
        category="linear",
        symbol=symbol,
        buyLeverage=leverage,
        sellLeverage=leverage,
    )
    print(f"Successfully set leverage to {leverage}x")