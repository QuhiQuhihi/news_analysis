#!/bin/bash
source ~/.bash_profile
cd ~/workspace/news_analysis

source .venv_news/bin/activate
python daily_job.py
