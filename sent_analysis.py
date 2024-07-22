from transformers import pipeline

def setup_sentiment_pipeline():
    model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_pipeline = pipeline('sentiment-analysis', model=model_name)
    return sentiment_pipeline

def analyze_sentiment(sentiment_pipeline, data):
    results = [sentiment_pipeline(str(text))[0] for text in data]  # Ensure text is a string
    scores = [1 if result['label'] == 'POSITIVE' else -1 for result in results]  # Convert to numerical scores
    return scores

def aggregate_sentiment(sentiments):
    score = sum(sentiments)  # Aggregate numerical scores
    return score
