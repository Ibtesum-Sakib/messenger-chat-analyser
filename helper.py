from nltk.sentiment import sentiment_analyzer
from urlextract import URLExtract
import pandas as pd
from collections import Counter
#import emoji
import regex as re
extract = URLExtract()

def fetch_stats(selected_sender,df):

    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]

        # 1. Fetching the number of messages
    num_messages = df.shape[0]

    # 2. Fetching the number of words
    words = []
    # str(x).split(".")
    for content in df['content']:
        words.extend(str(content).split())

    #Fetching number of media message
    num_of_media = df[df['type'] == "Share"].shape[0]
    #fetch number of links
    num_of_call = df[df['type'] == 'Call'].shape[0]


    return num_messages,len(words),num_of_media,num_of_call


def most_busy_users(df):
    x = df['sender_name'].value_counts().head()
    df = round((df['sender_name'].value_counts()/df.shape[0])*100,4).reset_index().rename(columns = {'index':'name','sender_name':'percentage'})
    return x,df

def most_msg_by_busy_user(df):
    x = df['sender_name'].value_counts().head()
    y = x.reset_index().rename(columns={'index': 'name', 'sender_name': 'total_msg'})
    z = y['total_msg'][0]
    return z

def most_common_words(selected_sender,df):
    f = open('stop_banglish.txt', 'r')
    stop_words = f.read()
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    words = []
    # str(x).split(".")
    for content in df['content']:
        for word in str(content).lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20)).rename(columns = {0:'word',1:'count'})
    return most_common_df

#def emoji_helper(selected_sender,df):
  #  if selected_sender != 'Overall':
   #     df = df[df['sender_name'] == selected_sender]
  #  emojis = []
  #  for message in df['content']:
   #     emojis.extend([c for c in str(message) if c in emoji.UNICODE_EMOJI['en']])
    #emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    #return emoji_df

def monthly_timeline(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    timeline = df.groupby(['year','month','month_name']).count()['content'].reset_index()

    times = []

    for time in range(timeline.shape[0]):
        times.append(timeline['month_name'][time] + "-" + str(timeline['year'][time]))
    timeline['time'] = times
    return timeline

def daily_timeline(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    daily_timeline = df.groupby('date_only').count()['content'].reset_index()

    return daily_timeline

def week_activity_map(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    return df['day_name'].value_counts()

def month_activity_map(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    return df['month_name'].value_counts()

def activity_heatmap(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='content', aggfunc='count').fillna(0)
    return user_heatmap

def most_messages_winner(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    df = round((df['sender_name'].value_counts() / df.shape[0]) * 100, 4).reset_index().rename(
        columns={'index': 'name', 'sender_name': 'percentage'})
    tf = df['name'].value_counts().head(1).reset_index()
    return tf['index'][0]

def most_wpm_winner(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    x = df.loc[df['hour'].idxmax()]
    return x['sender_name']

def max_msg_c(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    max_message_count = df['day_name'].value_counts().head(1).reset_index().rename(
        columns={'index': 'maxmsg_day', 'day_name': 'max_msg'})
    max_msgc = max_message_count['max_msg'][0]

    return max_msgc

def max_msg_d(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    max_message_count = df['day_name'].value_counts().head(1).reset_index().rename(
        columns={'index': 'maxmsg_day', 'day_name': 'max_msg'})
    max_msgd = max_message_count['maxmsg_day'][0]
    return max_msgd

def max_timeop(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    max_time = df.pivot_table(index='day_name', columns='period', values='content', aggfunc='count').fillna(0)
    max_period = max_time.max().reset_index().rename(columns={'period': 'period', 0: 'max_msg_onaperiod'})
    max_period_res = max_period.loc[max_period['max_msg_onaperiod'].idxmax()]
    r = max_period_res['period']
    return r

# It basically worked but slowing the whole process!
def sentiment_analysis(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    x = df.groupby(['month', 'year', 'sender_name']).mean().reset_index()
    y = x['sentiment'].values
    return y

def max_positivity(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    tf = df[['sentiment','sender_name']].max().reset_index()[0][1]
    return tf

def sn_num(selected_sender,df):
    if selected_sender != 'Overall':
        df = df[df['sender_name'] == selected_sender]
    tf = df[['sentiment','sender_name']].max().reset_index()[0][0]
    return tf
