import os
import sys

import numpy as np
import pandas as pd

from datetime import datetime

from news_collect import news_crawl
from news_data_insert import db_conn_test

def main_job():
    
    print("--- news crawling started ---")
    daily_news = news_crawl()
    news_data = daily_news.crawl_news_data()
    print("--- news crawling finished ---")

    print("--- insert to news_analysis started ---")
    db_conn_test(news_data)
    print("--- insert to news_analysis finished ---")

    print("--- insert to news_analysis finished ---")

if __name__=='__main__':
    print("daily job started")
    main_job()