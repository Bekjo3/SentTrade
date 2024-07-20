import schedule
import time
from set_newsapi import setup_newsapi, fetch_news
from set_praw import setup_reddit, scrape_reddit
from sent_analysis import setup_sentiment_pipeline, analyze_sentiment, aggregate_sentiment
from set_alpaca import setup_alpaca, trade_stock

# # Twitter API credentials
# twitter_bearer_token = 'AAAAAAAAAAAAAAAAAAAAABy%2FugEAAAAA%2FhKj7lzYcueScWU1HMLhQLQvnIo%3DLNCeOfSCT50De36cCHnb4UOoIqZGx1ALgEDkTOByrbwLzdWWwF'
# # twitter_api_key = 'dOGIwiHNrI5fj7huLdZ9lp7p2' # API KEY
# # twitter_api_secret_key = 'qeVimLjGf3VfaBRSpC3lDKNBie93KrrjnEwMPMbjMdssbITFR5'  # API KEY secret
# # twitter_access_token = '972557461285720064-gfErvkdsG4BRWkpmoSsHf2cycaJ7VSL' 
# # twitter_access_token_secret = 'jLdl60m5xxdSiR1HiXeq6wKl60c8zFDv0gRVzZag0NcDD' 

# Reddit API credentials
reddit_client_id='Z4r7dOwLw8A0fgFDAQZmmw',
reddit_client_secret='	95z4rLyIfC0I8jJ3kefcuLSmul2YLA',
reddit_user_agent='SentTrade'

# Alpaca API credentials
alpaca_api_key = 'PKA6P2IYLJF6QXFC9TX4'
alpaca_secret_key = 'lrkfeZ9c6jh3S4ge4Gx9dJks9VgIeBVuBoIy11QF'

# News API
newsapi_key = '3197f525f664448abd31cb5b0ad6e6b3'

# Setup APIs
newsapi = setup_newsapi(newsapi_key)
reddit = setup_reddit(reddit_client_id, reddit_client_secret, reddit_user_agent)
alpaca = setup_alpaca(alpaca_api_key, alpaca_secret_key)
sentiment_pipeline = setup_sentiment_pipeline()

# List of stocks to analyze
stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']

def job():
    best_stock = None
    best_score = float('-inf')

    for stock in stocks:
        try:
            reddit_data = scrape_reddit(reddit, 'stocks', stock)
        except Exception as e:
            print(f"Error fetching reddit posts: {e}")
            reddit_data = []

        try:
            news_data = fetch_news(newsapi, stock)
        except Exception as e:
            print(f"Error fetching news: {e}")
            news_data = []

        combined_data = reddit_data + news_data
        if not combined_data:
            print(f"No data for stock {stock}")
            continue

        try:
            sentiments = analyze_sentiment(sentiment_pipeline, combined_data)
            sentiment_score = aggregate_sentiment(sentiments)
        except Exception as e:
            print(f"Error analyzing sentiment for {stock}: {e}")
            sentiment_score = 0

        print(f"Stock: {stock}, Sentiment Score: {sentiment_score}")

        if sentiment_score > best_score:
            best_score = sentiment_score
            best_stock = stock

    if best_stock:
        try:
            trade_stock(alpaca, best_score, best_stock)
            print(f"Traded Stock: {best_stock}, Score: {best_score}")
        except Exception as e:
            print(f"Error trading stock {best_stock}: {e}")

# schedule.every().day.at('09:00').do(job)
# testing
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)