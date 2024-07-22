import requests

def setup_news_api(api_key):
    return {'api_key': api_key}

def scrape_news(news_client, asset, from_date, to_date):
    api_key = news_client['api_key']
    url = f'https://newsapi.org/v2/everything?q={asset}&from={from_date}&to={to_date}&apiKey={api_key}'
    response = requests.get(url)
    response_json = response.json()
    if response.status_code == 200:
        return [article['title'] for article in response_json['articles']]
    else:
        raise Exception(f"Error fetching news: {response_json['message']}")
