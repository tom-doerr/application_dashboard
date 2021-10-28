#!/usr/bin/env python3

'''
This script creates a backup by saving all the data in the database as a csv file.
'''


import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlalchemy
from sqlalchemy import create_engine
import altair as alt
from sqlalchemy import select

TIME_ZONE_DIFF = 2


db_url = st.secrets['db_url']

def connect_to_database():
    # Connect
    import sqlalchemy
    engine = sqlalchemy.create_engine(db_url)
    engine.connect()

    from sqlalchemy import MetaData
    meta = MetaData()
    meta.reflect(bind=engine)

    return engine, meta

engine, meta = connect_to_database()


# Print all the data from table api_appform.
from sqlalchemy import select
conn = engine.connect()
s = select([meta.tables['api_appform']])
result = conn.execute(s)
for row in result:
    print(row)


# Save all the data in a CSV file
df = pd.read_sql_table('api_appform', engine)

df.to_csv('data.csv', index=False)

