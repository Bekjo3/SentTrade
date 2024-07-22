import schedule
import time
from set_newsapi import setup_news_api, scrape_news
from set_praw import setup_reddit, scrape_reddit
from sent_analysis import setup_sentiment_pipeline, analyze_sentiment, aggregate_sentiment
from set_alpaca import setup_alpaca, trade_stock, get_historical_data, backtest_strategy

# Reddit API credentials
reddit_client_id=''
reddit_client_secret=''
reddit_user_agent=''
reddit_username = ''
reddit_password = ''

# Alpaca API credentials
alpaca_api_key = ''
alpaca_secret_key = ''

# News API
news_api_key = ''

# Setup APIs
news_client = setup_news_api(news_api_key)
reddit = setup_reddit(reddit_client_id, reddit_client_secret, reddit_user_agent, reddit_username, reddit_password)
alpaca = setup_alpaca(alpaca_api_key, alpaca_secret_key)
sentiment_pipeline = setup_sentiment_pipeline()

# List of stocks to analyze
stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'NVDA', 'META', 'DIS', 'WMT', 'NFLX']

def job():
    best_stock = None
    best_score = float('-inf')
    overall_negative = True

    for stock in stocks:
        try:
            reddit_data = scrape_reddit(reddit, 'stocks', stock, limit=50)
            print(f"Reddit data for {stock} fetched successfully.")
        except Exception as e:
            print(f"Error fetching Reddit data for {stock}: {e}")
            reddit_data = []

        try:
            news_data = scrape_news(news_client, stock)
            print(f"News data for {stock} fetched successfully.")
        except Exception as e:
            print(f"Error fetching news data for {stock}: {e}")
            news_data = []

        try:
            combined_data = reddit_data + news_data

            if combined_data:
                sentiments = analyze_sentiment(sentiment_pipeline, combined_data)
                sentiment_score = aggregate_sentiment(sentiments)

                print(f"Stock: {stock}, Sentiment Score: {sentiment_score}")

                if sentiment_score > best_score:
                    best_score = sentiment_score
                    best_stock = stock

                if sentiment_score > 0:
                    overall_negative = False
        except Exception as e:
            print(f"Error processing sentiment for {stock}: {e}")

    if best_stock and not overall_negative:
        trade_stock(alpaca, best_score, best_stock)
        print(f"Traded Stock: {best_stock}, Score: {best_score}")

def backtest():
    for stock in stocks[:5]:  # Limit to 5 stocks to reduce API calls
        try:
            performance_metrics = backtest_strategy(alpaca, sentiment_pipeline, news_client, reddit, stock, '2024-06-21', '2024-07-05')
            print(f"Backtest Performance for {stock}: {performance_metrics}")
        except Exception as e:
            print(f"Error backtesting stock {stock}: {e}")

# Schedule job
# schedule.every().day.at('09:00').do(job)
# testing
schedule.every(1).minutes.do(job)

# Testing backtest
backtest()

while True:
    schedule.run_pending()
    time.sleep(1)