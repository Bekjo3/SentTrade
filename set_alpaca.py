from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
from set_newsapi import scrape_news
from set_praw import scrape_reddit

def setup_alpaca(api_key, secret_key, base_url='https://paper-api.alpaca.markets'):
    alpaca = REST(api_key, secret_key, base_url)
    return alpaca

def get_current_positions(alpaca):
    positions = alpaca.list_positions()
    return {position.symbol: int(position.qty) for position in positions}

def calculate_risk_management_levels(sentiment_score):
    if sentiment_score > 0:
        take_profit = sentiment_score * 1.5
        stop_loss = -sentiment_score / 1.5
    else:
        take_profit = sentiment_score / 1.5
        stop_loss = sentiment_score * 1.5
    return take_profit, stop_loss

def trade_stock(alpaca, sentiment_score, stock_symbol, min_sentiment_threshold=-5):
    positions = get_current_positions(alpaca)
    take_profit, stop_loss = calculate_risk_management_levels(sentiment_score)

    if sentiment_score > 0:
        alpaca.submit_order(
            symbol=stock_symbol,
            notional=1000,
            side='buy',
            type='market',
            time_in_force='gtc',
            order_class='bracket',
            take_profit=dict(limit_price=take_profit),
            stop_loss=dict(stop_price=stop_loss)
        )
    elif sentiment_score < min_sentiment_threshold and stock_symbol in positions and positions[stock_symbol] > 0:
        alpaca.submit_order(
            symbol=stock_symbol,
            qty=positions[stock_symbol],
            side='sell',
            type='market',
            time_in_force='gtc'
        )

def get_historical_data(alpaca, stock_symbol, start_date='2024-06-21', end_date='2024-07-05'):
    bars = alpaca.get_bars(stock_symbol, TimeFrame.Day, start=start_date, end=end_date).df
    return bars

def backtest_strategy(alpaca, sentiment_pipeline, news_client, reddit, stock_symbol, start_date='2024-06-21', end_date='2024-07-05'):
    historical_data = get_historical_data(alpaca, stock_symbol, start_date, end_date)
    dates = historical_data.index.tolist()

    performance = []
    news_data_cache = {}

    for date in dates:
        from_date = (date - pd.Timedelta(days=14)).strftime('%Y-%m-%d')
        to_date = date.strftime('%Y-%m-%d')

        if from_date not in news_data_cache:
            try:
                news_data = scrape_news(news_client, stock_symbol, from_date, to_date)
                news_data_cache[from_date] = news_data
            except Exception as e:
                print(f"Error fetching news for backtesting {stock_symbol}: {e}")
                news_data_cache[from_date] = []

        try:
            reddit_data = scrape_reddit(reddit, 'stocks', stock_symbol, from_date, to_date)
            combined_data = news_data_cache[from_date] + reddit_data

            if combined_data:
                sentiments = analyze_sentiment(sentiment_pipeline, combined_data)
                sentiment_score = aggregate_sentiment(sentiments)
                performance.append((date, sentiment_score))
        except Exception as e:
            print(f"Error fetching Reddit data for backtesting {stock_symbol}: {e}")

    returns = []
    buy_price = None
    for i in range(1, len(performance)):
        date, sentiment_score = performance[i]
        prev_date, prev_sentiment_score = performance[i - 1]

        if sentiment_score > 0 and (prev_sentiment_score is None or prev_sentiment_score <= 0):
            buy_price = historical_data.loc[prev_date]['close']
        elif sentiment_score <= 0 and buy_price is not None:
            sell_price = historical_data.loc[prev_date]['close']
            returns.append((sell_price - buy_price) / buy_price)
            buy_price = None

    if len(returns) == 0:
        roi = 0
        sharpe_ratio = 0
    else:
        roi = sum(returns)
        sharpe_ratio = (pd.Series(returns).mean() / pd.Series(returns).std()) * (252 ** 0.5) if pd.Series(returns).std() != 0 else 0

    drawdown = (historical_data['close'].cummax() - historical_data['close']).max()
    win_rate = len([r for r in returns if r > 0]) / len(returns) if len(returns) != 0 else 0

    performance_metrics = {
        'ROI': roi,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown': drawdown,
        'Win Rate': win_rate
    }
    return performance_metrics
