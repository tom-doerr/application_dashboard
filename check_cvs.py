#!/usr/bin/env python3

'''
This script checks whether there are duplicate values in the resume field and lists the 
names and ids of the users in the database.
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






if False:
    for table in meta.tables:
        print(table)

    # Print all the data from table api_appform.
    from sqlalchemy import select
    conn = engine.connect()
    s = select([meta.tables['api_appform']])
    result = conn.execute(s)
    for row in result:
        print(row)

    # Print all the field descriptions from the table api_appform
    from sqlalchemy import inspect
    inspector = inspect(engine)
    for column in inspector.get_columns('api_appform'):
        print(column['name'], column['type'])



# Check for duplicate values in the resume field.
def get_duplicate_resumes(engine, meta):
    conn = engine.connect()
    s = select([meta.tables['api_appform']])
    result = conn.execute(s)

    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    df.info()

    # Create a dataframe with just the resumes.
    df_resumes = df.filter(regex='resume')
    df_resumes.info()
    print("df_resumes:", df_resumes)

    # Remove duplicate entries.
    df_resumes_unique = df_resumes.drop_duplicates()
    df_resumes_unique.info()
    print("df_resumes_unique:", df_resumes_unique)

    # Get ids of duplicate entries.
    df_resumes_duplicate = df_resumes[df_resumes.duplicated(keep=False)]
    df_resumes_duplicate.info()
    print("df_resumes_duplicate:", df_resumes_duplicate)
    return df_resumes_duplicate



def list_all_entries_with_cv_name(name):
    conn = engine.connect()
    s = select([meta.tables['api_appform']])
    result = conn.execute(s)

    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    df.info()

    # Create a dataframe with just the resumes.
    df_resumes = df.filter(regex='resume')
    df_resumes.info()

    # Filter for name.
    df_resumes_name = df_resumes[df_resumes['resume'].str.contains(name)]
    df_resumes_name.info()
    df_resumes_name.head()
    print("df_resumes_name:", df_resumes_name)




list_all_entries_with_cv_name('CV.pdf')
print('===================================')
df_resumes_duplicate = get_duplicate_resumes(engine, meta)

indices_duplicate = df_resumes_duplicate.index.values.tolist()


indices_duplicate = [i for i in indices_duplicate]
print("indices_duplicate:", indices_duplicate)


conn = engine.connect()
s = select([meta.tables['api_appform']])
result = conn.execute(s)

df = pd.DataFrame(result.fetchall())
df.columns = result.keys()
print("df:", df)



# Get ids for indices in indices_duplicate.
df_ids = df.iloc[indices_duplicate]
df_ids.info()
print("df_ids:", df_ids)




