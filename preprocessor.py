import re

import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def preprocess(data):
    messages = pd.DataFrame(data['messages'])
    messages['date'] = messages['timestamp_ms'].apply(convert_time)
    messages['date_only'] = messages['date'].dt.date
    messages['year'] = messages['date'].dt.year
    messages['month_name'] = messages['date'].dt.month_name()
    messages['month'] = messages['date'].dt.month
    messages['day'] = messages['date'].dt.day
    messages['day_name'] = messages['date'].dt.day_name()
    messages['hour'] = messages['date'].dt.hour
    messages['minute'] = messages['date'].dt.minute
    messages['sentiment'] = messages['content'].apply(get_polarity)



    period = []
    for hour in messages[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    messages['period'] = period

    return messages

def convert_time(timestamp):
    return pd.to_datetime(timestamp, unit='ms')
def get_polarity(text):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    return sentiment_analyzer.polarity_scores(str(text))['compound']