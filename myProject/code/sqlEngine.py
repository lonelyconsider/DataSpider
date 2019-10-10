# -*- coding:utf-8 -*-

# import pyodbc
import pymssql
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# Create on 2018/5/26
# By leslie


def sql_engine():
    try:
        engine = create_engine('mssql+pymssql://sa:123456@127.0.0.1:1433/devDWH')  # staging
        print('Connect to sql-server successful !')
        return engine
    except Exception as e:
        print(e)
        pass



