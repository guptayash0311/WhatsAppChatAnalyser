from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    # 1. Fetch number of messages
    num_messages = df.shape[0]
    # 2. Fetch number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
        
    # 3. Fetch number of media messages
    num_media_messages = df[df['message']=='<Media omitted>\n'].shape[0]
    
    # 4. Fetch number of Links
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
        
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x=df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'users':'name','count':'percent'})
    return x, df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    
    temp=df[df['users'] != 'group_notification']
    temp=temp[temp['message']!='<Media omitted>']
    
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df['users']==selected_user]
    
    temp=df[df['users'] != 'group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
                
        