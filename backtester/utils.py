# backtester/utils.py
import pandas as pd
from data_fetcher.models import StockData

def calculate_moving_average(data, window):
    return data['close_price'].rolling(window=window).mean()

def backtest_strategy(symbol, initial_investment, short_window, long_window):
    data = StockData.objects.filter(symbol=symbol).order_by('date')
    df = pd.DataFrame(list(data.values()))

    df['short_ma'] = calculate_moving_average(df, short_window)
    df['long_ma'] = calculate_moving_average(df, long_window)

    df['position'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'position'] = 1
    df.loc[df['short_ma'] < df['long_ma'], 'position'] = -1

    df['returns'] = df['close_price'].pct_change()
    df['strategy_returns'] = df['position'].shift(1) * df['returns']

    cumulative_returns = (1 + df['strategy_returns']).cumprod()
    total_return = cumulative_returns.iloc[-1] - 1
    max_drawdown = (cumulative_returns / cumulative_returns.cummax() - 1).min()
    num_trades = (df['position'].diff() != 0).sum() / 2

    return {
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'num_trades': num_trades
    }