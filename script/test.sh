#!/bin/bash

time_stamp=`date +%Y/%m/%d/%H:%M`
echo "It is ${time_stamp}, daily_job start"

cd /home/ubuntu/workspace/news_analysis 

source /home/ubuntu/workspace/news_analysis/.venv_news/bin/activate 
python /home/ubuntu/workspace/news_analysis/test.py >> /home/ubuntu/log/test/date_$(date "+%Y-%m-%d").log

echo "It is ${time_stamp} , crontab news_daily_job success." 