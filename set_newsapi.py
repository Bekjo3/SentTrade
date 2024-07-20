from newsapi import NewsApiClient

def setup_newsapi(api_key):
    newsapi = NewsApiClient(api_key=api_key)
    return newsapi

def fetch_news(newsapi, keyword):
    try:
        all_articles = newsapi.get_everything(q=keyword, language='en', sort_by='relevancy', page_size=5)
        articles = all_articles.get('articles', [])
        return [article['title'] + ' ' + article['description'] for article in articles if article['title'] and article['description']]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
