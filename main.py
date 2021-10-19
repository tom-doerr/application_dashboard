#!/usr/bin/env python3

'''
This script connects to a PostgreSQL database  and 
visualizes the data using streamlit.
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

# @st.cache(allow_output_mutation=True)
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


# Plot the total number of applications over time
st.title('Total number of applications received over time')
st.write('''
The total number of applications received over time.
''')

import datetime

# Get the dates from the table that is stored in the submitted_at field.
from sqlalchemy import extract
conn = engine.connect()
s = select([meta.tables['api_appform'].c.submitted_at])
result = conn.execute(s)
dates = [x['submitted_at'] for x in result]

df = pd.DataFrame(dates, columns=['dates'])
# Sort the df by dates.
df['dates'] = pd.to_datetime(df['dates'])
df = df.sort_values(by=['dates'])

totals = 0
date_counts_list = []
for date in df['dates']:
    df['dates'] = pd.to_datetime(df['dates'])
    totals += 1
    date_counts_list.append((date, totals))


# Plot the total number of applications over time
df = pd.DataFrame(date_counts_list, columns=['dates', 'count'])
# convert the dates to strings.
df['dates'] = df['dates'].dt.strftime('%d. %H:%M')

# Add the value in TIME_ZONE_DIFF as hours to all values in df.dates.
df['dates'] = df['dates'].apply(lambda x: datetime.datetime.strptime(x, '%d. %H:%M') + datetime.timedelta(hours=TIME_ZONE_DIFF))




# Plot the data with the dates on the x axis and count on y
st.altair_chart(
    alt.Chart(df).mark_line().encode(
        x='dates',
        y='count'))



# Count the number of entries in the table
from sqlalchemy import func
conn = engine.connect()
s = select([func.count(meta.tables['api_appform'].c.id)])
result = conn.execute(s)
count = result.fetchone()[0]

st.write(f'''
Number of applications received: {count}
''')


# Count the number of nationalities.
# Get the nationalities from the table that is stored in the nationality field.
from sqlalchemy import extract
conn = engine.connect()
s = select([meta.tables['api_appform'].c.nationality])
result = conn.execute(s)
nationalities = [x['nationality'] for x in result]

# Count the number of unique nationalities.
import pandas as pd
df = pd.DataFrame(nationalities, columns=['nationalities'])
df['count'] = 1
df = df.groupby('nationalities')['count'].sum()

num_nationalities = len(df)

st.write(f'''
Number of nationalities: {num_nationalities}
''')


# Count the number of languages.
# Get the languages from the table that is stored in the languages field.
# Each participant can have multiple languages that are stored as a string
# with the languages sepearted as a column, e.g. "German,English"
from sqlalchemy import extract
conn = engine.connect()
s = select([meta.tables['api_appform'].c.languages])
result = conn.execute(s)
languages = [x['languages'] for x in result]

# Split languages on comma.
languages_list = []
for language in languages:
    language_list = language.split(',')
    languages_list.extend(language_list)

# Count the number of unique languages.
import pandas as pd
df = pd.DataFrame(languages_list, columns=['languages'])
df['count'] = 1
df = df.groupby('languages')['count'].sum()

num_languages = len(df)

st.write(f'''
Number of languages: {num_languages}
''')





# Get the dates from the table that is stored in the submitted_at field.
from sqlalchemy import extract
conn = engine.connect()
s = select([meta.tables['api_appform'].c.submitted_at])
result = conn.execute(s)
dates = [x['submitted_at'] for x in result]


# Plot gender from the table.
st.title('Gender of applicants')
st.write('''
The gender of applicants.
''')

from sqlalchemy import func
conn = engine.connect()
s = select([meta.tables['api_appform'].c.gender])
result = conn.execute(s)
genders = [x['gender'] for x in result]

df = pd.DataFrame(genders, columns=['gender'])
df['count'] = 1
df = df.groupby('gender')['count'].sum()
st.bar_chart(df)

# Plot age from the table.
st.title('Age of applicants')
st.write('''
The age of applicants.
''')

from sqlalchemy import func
conn = engine.connect()
s = select([meta.tables['api_appform'].c.age])
result = conn.execute(s)
ages = [x['age'] for x in result]

df = pd.DataFrame(ages, columns=['age'])
df['count'] = 1
df = df.groupby('age')['count'].sum()
st.bar_chart(df)


# Plot the hours type from the table.
st.title('Hours applicants want to spend')
st.write('''
The hours applicants want to spend.
''')

from sqlalchemy import func
conn = engine.connect()
s = select([meta.tables['api_appform'].c.hours])
result = conn.execute(s)
hours_types = [x['hours'] for x in result]

df = pd.DataFrame(hours_types, columns=['hours'])
df['count'] = 1
df = df.groupby('hours')['count'].sum()
st.bar_chart(df)



# Plot the semester type from the table.
st.title('Semester of applicants')
st.write('''
The semester of applicants.
''')

# get the degree and semester in one query.
conn = engine.connect()
s = select([meta.tables['api_appform'].c.degree, meta.tables['api_appform'].c.semester])
result = conn.execute(s)
degree_semesters = [(x['degree'], x['semester']) for x in result]


degree_semester_joined = []
for degree_semester in degree_semesters:
    degree_semester_joined.append(degree_semester[0] + ' - ' + degree_semester[1])

df = pd.DataFrame(degree_semester_joined, columns=['degree_semester'])
df['count'] = 1
df = df.groupby('degree_semester')['count'].sum()
st.bar_chart(df)




# Plot the degree type from the table.
st.title('Degree of applicants')
st.write('''
The degree of applicants.
''')

from sqlalchemy import func
conn = engine.connect()
s = select([meta.tables['api_appform'].c.degree])
result = conn.execute(s)
degree_types = [x['degree'] for x in result]

df = pd.DataFrame(degree_types, columns=['degree'])
df['count'] = 1
df = df.groupby('degree')['count'].sum()
st.bar_chart(df)





# Plot the university type from the table.
st.title('University of applicants')
st.write('''
The university of applicants.
''')

from sqlalchemy import func
conn = engine.connect()
s = select([meta.tables['api_appform'].c.university])
result = conn.execute(s)
university_types = [x['university'] for x in result]

df = pd.DataFrame(university_types, columns=['university'])
df['count'] = 1
df = df.groupby('university')['count'].sum()
st.bar_chart(df)



# Plot the languages of the applicants.
st.title('Languages of applicants')
st.write('''
The languages of applicants.
''')

from sqlalchemy import func
conn = engine.connect()
s = select([meta.tables['api_appform'].c.languages])
result = conn.execute(s)
languages = [x['languages'].split(',') for x in result]

languages = [item for sublist in languages for item in sublist]

df = pd.DataFrame(languages, columns=['languages'])
df['count'] = 1
df = df.groupby('languages')['count'].sum()
st.bar_chart(df)


# Plot the nationalities of the applicants.
st.title('Nationalities of applicants')
st.write('''
The nationalities of applicants.
''')

from sqlalchemy import func
conn = engine.connect()
s = select([meta.tables['api_appform'].c.nationality])
result = conn.execute(s)
nationalities = [x['nationality'].split(',') for x in result]

nationalities = [item for sublist in nationalities for item in sublist]

df = pd.DataFrame(nationalities, columns=['nationality'])
df['count'] = 1
df = df.groupby('nationality')['count'].sum()
st.bar_chart(df)



# Plot the number of applications per day of the week
st.title('Number of applications received per day of the week')
st.write('''
The number of applications received per day of the week.
''')

import datetime


# Get the dates from the table that is stored in the submitted_at field.
from sqlalchemy import extract
conn = engine.connect()
s = select([meta.tables['api_appform'].c.submitted_at])
result = conn.execute(s)
dates = [x['submitted_at'] for x in result]

# Convert the dates into a list of day of the week.
import pandas as pd
df = pd.DataFrame(dates, columns=['dates'])
df['dates'] = pd.to_datetime(df['dates'])
df['day_of_week'] = df['dates'].dt.day_name()
df['count'] = 1
df = df.groupby('day_of_week')['count'].sum()
st.bar_chart(df)



# Plot the hour the application was submitted.
st.title('Hour of the day the application was submitted')
st.write('''
The hour of the day the application was submitted.
''')

# Get the hours from the table that is stored in the submitted_at field.
from sqlalchemy import extract
conn = engine.connect()
s = select([meta.tables['api_appform'].c.submitted_at])
result = conn.execute(s)

hours = [x['submitted_at'].hour for x in result]

# Add the value in TIME_ZONE_DIFF as hours to all values in hours.
hours = [x + TIME_ZONE_DIFF for x in hours]


# Plot the data
df = pd.DataFrame(hours, columns=['hours'])
df['count'] = 1
df = df.groupby('hours')['count'].sum()

st.bar_chart(df)



