from pybit.unified_trading import HTTP
from .config import API_KEY, API_SECRET

# define global parameters
symbol = "SOLUSDT"
leverage = "10"
qty = 1  # place 1 contract per order
step_size_down = 0.75
step_size_up = 0.75 # place limit orders every 0.5 dollar of price change
max_entry_size = 5 # maximum entry size in contracts
trading_timer = 900 #900 # reshuffle trades every 15 minutes


session = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET,
)