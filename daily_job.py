import os
import sys

import numpy as np
import pandas as pd

from datetime import datetime

from news_collect import news_crawl
from news_data_insert import insert_news_data


class daily_job():
    def __init__(self, today=None) -> None:
        
        if today == None:
            today = datetime.datetime.today()
            today = today.strftime('%Y-%m-%d')
    
    def main_job(self, today):
        
        print("--- news crawling started ---")
        news_data = news_crawl.crawl_news_data()
        print("--- news crawling finished ---")

        print("--- insert to news_analysis started ---")
        insert_news_data.db_conn_test(news_data)
        print("--- insert to news_analysis finished ---")

if __name__=='__main__':
    daily_job.main_job()


