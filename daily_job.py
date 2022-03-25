import os
import sys

import numpy as np
import pandas as pd

from datetime import datetime

from news_collect import news_crawl
from news_data_insert import db_conn_test


class daily_job:
    def __init__(self, today=None):
        
        if today == None:
            today = datetime.today()
            self.today = today.strftime('%Y-%m-%d')
        
        self.base_dir = os.getcwd()
        self.data_dir = os.path.join(self.base_dir,'data')
        self.news_dir = os.path.join(self.data_dir,'news')
    
    def main_job(self):
        
        print("--- news crawling started ---")
        news_data = news_crawl.crawl_news_data()
        print("--- news crawling finished ---")
        print("--- insert to news_analysis started ---")
        insert_news_data.db_conn_test(news_data)
        print("--- insert to news_analysis finished ---")

        print("--- insert to news_analysis finished ---")

if __name__=='__main__':
    day_job = daily_job('2022-03-25')
    day_job.main_job()


