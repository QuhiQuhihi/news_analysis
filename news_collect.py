import os
import sys
import sqlite3
import calendar
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

import nltk
# nltk.download('punkt')
from bs4 import BeautifulSoup
from newspaper import Article
from newscatcher import Newscatcher, describe_url, urls

class news_crawl:
    def __init__(self):
        self.now = datetime.today()
        self.now_1d = datetime.today() - timedelta(days=1)
        self.today = datetime.today().strftime("%Y-%m-%d %H:%M")
        self.yesterday = (self.now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")

        # self.yesterday = datetime.today() - timedelta(days=1)
        
        self.news_dir = os.path.join(os.getcwd(),'data','news')
        
        self.news_topic = ['tech', 'news', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world']
        self.news_url = {
                        'newyork_times': 'nytimes.com',
                        'washington_post':'washingtonpost.com',
                        # 'wallstreet_journal':'wsj.com',
                        # 'bloomberg':'bloomberg.com',
                        'cnn':'cnn.com',
                        'cnbc':'cnbc.com',
                        'financial_times':'ft.com/',
                        # 'reuters':'reuters.com'
                    }
        self.news_url_list = list(self.news_url.values())


    def crawl_news_data(self):

    # [source, topic, title, publish_date, link, text]
    # link = news_url, newspaper3k package will load news contents
    # link from newscatcher, text from newspaper3k
        news_base_data = []
        number = 0

        for base_url in self.news_url_list:
            
            number += 1
            print(number, base_url)
            
            # topics of base_url
            topics = describe_url(base_url)['topics']
            
            # loop each topics
            try:
                for topic in topics:
                    nc = Newscatcher(base_url, topic = topic)
                    results = nc.get_news()
                    articles = results['articles']

                    # base_url - topic pair
                    for article in articles:
                        title = article['title']
                        pub_date = article['published']
                        link = article['link']

                        temp = []

                        temp.append(base_url)
                        temp.append(topic)
                        temp.append(title)
                        temp.append(pub_date)
                        temp.append(link)

                        news_base_data.append(temp)

            except:
                print(base_url, topic, title)

        df_news_base_data = pd.DataFrame(news_base_data, columns=['source','topic','title','publish_date','link'])

        # filter last 24 hour news
        df_news_base_data = df_news_base_data.query(f"publish_date > '{self.yesterday}' and publish_date < '{self.now}'")
        df_news_base_data = df_news_base_data.reset_index(drop=True)

        df_news_base_data['date'] = datetime.today().strftime("%Y-%m-%d")
        df_news_base_data['keyword'] = ''
        df_news_base_data['text'] = ''

        try:
            for i in df_news_base_data.index:
                print(i, df_news_base_data.loc[i,'source'], df_news_base_data.loc[i,'title'])
                
                # datetime conversion for publish date to 2022-03-22 09:00 format
                _str_datetime = df_news_base_data.loc[i,'publish_date'][:22]
                _stf_datetime = datetime.strptime(_str_datetime, '%a, %d %b %Y %H:%M')
                datetime_str = datetime.strftime(_stf_datetime, '%Y-%m-%d %H:%M')
                
                df_news_base_data.loc[i,'publish_date'] = datetime_str

                url = df_news_base_data.loc[i, 'link']
                article = Article(df_news_base_data.loc[i,'link'], language='en')

                article.download()
                article.parse()
                article.nlp()

                title, keywords, text = article.title, article.keywords, article.text

                keyword_str = ''
                for keyword in keywords:
                    keyword_str = keyword_str + keyword + '/'

                df_news_base_data.loc[i ,'keyword'] = keyword_str
                df_news_base_data.loc[i ,'text'] = text
                    
        except:
            print(i, df_news_base_data.loc[i,'source'], df_news_base_data.loc[i,'title'])
        
        # filter last 24 hour news
        df_news_base_data = df_news_base_data[['source','topic','title','publish_date','link','date','keyword','text']]
        df_news_base_data.to_excel(os.path.join(self.news_dir,f'{self.now.strftime("%Y-%m-%d")}_news.xlsx'))
        return df_news_base_data
        
if __name__=="__main__":
    news_today = news_crawl()
    df_news = news_today.crawl_news_data()