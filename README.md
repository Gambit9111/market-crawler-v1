# Algo Trading Bot

This is an algorithmic trading bot that uses the Binance API to execute trades based on certain conditions. The bot uses the APScheduler library to schedule trades at regular intervals.

## Features

- **Limit Buy and Sell Orders**: The bot sets limit buy and sell orders based on the current ask and bid prices + step size.
- **Leverage Management**: The bot manages the leverage for each trade.
- **Position Management**: The bot manages the current position quantity and sets buy and sell orders accordingly.
- **Scheduled Trades**: The bot executes trades at regular intervals using APScheduler.
