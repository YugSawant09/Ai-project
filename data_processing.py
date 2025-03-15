import pandas as pd
import json
from datetime import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Log user queries in CSV
def log_query_csv(query):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sentiment_score = sia.polarity_scores(query)["compound"]
    sentiment = "positive" if sentiment_score > 0.05 else "negative" if sentiment_score < -0.05 else "neutral"
    df = pd.DataFrame([[timestamp, query, sentiment]], columns=["timestamp", "query", "sentiment"])
    df.to_csv("logs/user_queries.csv", mode='a', header=False, index=False)

# Log user queries in JSON
def log_query_json(query):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sentiment_score = sia.polarity_scores(query)["compound"]
    sentiment = "positive" if sentiment_score > 0.05 else "negative" if sentiment_score < -0.05 else "neutral"
    log_entry = {"timestamp": timestamp, "query": query, "sentiment": sentiment}

    with open("logs/user_queries.json", "r+") as file:
        data = json.load(file)
        data.append(log_entry)
        file.seek(0)
        json.dump(data, file, indent=4)

# Function to retrieve query history
def get_query_history():
    try:
        df = pd.read_csv("logs/user_queries.csv")
        return df.tail(10)  # Show last 10 queries
    except Exception as e:
        return str(e)
