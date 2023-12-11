from bot import session, symbol, qty, step_size_down, step_size_up, max_entry_size, trading_timer, leverage
from .functions import ask_bid, open_long_position, close_long_position, get_current_position, set_leverage, cancel_all_orders

from apscheduler.schedulers.blocking import BlockingScheduler


def do_trades():
    cancel_all_orders(session, symbol)
    ask, bid = ask_bid(session, symbol)
    current_position_qty = get_current_position(session, symbol)[3]
    
    print(f"ask: {ask}, bid: {bid}, current_position_qty: {current_position_qty}, trading_timer: {trading_timer} seconds")
    
    if current_position_qty == 0:
        print(f"set {max_entry_size} limit buy orders bellow the price in steps of {step_size_down} dollar")
        for i in range(1, max_entry_size + 1):
            open_long_position(session, symbol, "Limit", qty, bid - i * step_size_down)
    
    elif current_position_qty == max_entry_size:
        print(f"set {max_entry_size} limit sell orders above the price in steps of {step_size_up} dollar")
        for i in range(1, max_entry_size + 1):
            close_long_position(session, symbol, "Limit", qty, ask + i * step_size_up)
    
    elif current_position_qty > 0 and current_position_qty < max_entry_size:
        position_size_left = max_entry_size - current_position_qty
        print(f"set {position_size_left} limit buy orders bellow the price in steps of {step_size_down} dollar")
        for i in range(1, int(position_size_left) + 1):
            open_long_position(session, symbol, "Limit", qty, bid - i * step_size_down)
        
        print(f"set {current_position_qty} limit sell orders above the price in steps of {step_size_up} dollar")
        for i in range(1, int(current_position_qty) + 1):
            close_long_position(session, symbol, "Limit", qty, ask + i * step_size_up)
    
    else:
        print("all positions are filled, waiting")
    
    print("reshuffle trades")

def demo():
    print("demo")

def main():
    """ main function
    """

    try:
        set_leverage(session, symbol, leverage)
    except Exception as e:
        print(e)
    
    
    scheduler = BlockingScheduler()
    scheduler.add_job(do_trades, 'interval', seconds=trading_timer)
    scheduler.start()



if __name__ == "__main__":
    main()