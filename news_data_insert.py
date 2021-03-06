import os
import sys
import datetime
import traceback
import numpy as np
import pandas as pd

from config import aws_rds_config

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

def create_db_engine(config: aws_rds_config) -> Engine:
    url = 'postgresql://{user}:{password}@{host}:{port}/{db}'
    url = url.format(
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        db=config.dbname,
    )
    return create_engine(url)


def create_db_session(engine: Engine):
    session = sessionmaker(bind=engine, autocommit=False)
    return session

def db_conn_test(df_insert):

    config = aws_rds_config()
    db_engine = create_db_engine(config=config)  # DB 엔진 정의
    db_engine.connect()  # DB 커넥션 생성
    session = create_db_session(engine=db_engine)  # DB 세션 생성
    df_insert.loc[:,'created_at'] = datetime.datetime.now()
    df_insert.loc[:,'updated_at'] = datetime.datetime.now()


    try:
        session = session()  # SQLAlchemy 에서 사용할 세션 정의
        df_insert.to_sql('news_data', con=db_engine, schema='public', if_exists='append', index=False,
                dtype={
                    'date': sqlalchemy.VARCHAR(100),
                    'publish_date': sqlalchemy.DATETIME(),
                    'news_source': sqlalchemy.VARCHAR(100),
                    'news_topic': sqlalchemy.VARCHAR(100),
                    'news_title': sqlalchemy.VARCHAR(100),
                    'news_keyword': sqlalchemy.VARCHAR(100),
                    'news_link': sqlalchemy.VARCHAR(100),
                    'news_text' : sqlalchemy.TEXT(),
                    'created_at':sqlalchemy.DATETIME(),
                    'updated_at': sqlalchemy.DATETIME()
                })
    except Exception as error:
        print("db error")
        # raise error
        msg = '{}'.format(traceback.format_exc())
        print(msg)

    finally:
        session.close()  # DB 세션 닫기