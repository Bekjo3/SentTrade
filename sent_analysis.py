from transformers import pipeline

def setup_sentiment_pipeline():
    model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_pipeline = pipeline('sentiment-analysis', model=model_name)
    return sentiment_pipeline

def analyze_sentiment(sentiment_pipeline, data):
    return [sentiment_pipeline(text)[0] for text in data]

def aggregate_sentiment(sentiments):
    positive = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
    negative = sum(1 for s in sentiments if s['label'] == 'NEGATIVE')
    score = positive - negative
    return score
