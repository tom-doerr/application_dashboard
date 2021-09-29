#!/usr/bin/env python3

'''
This script reads in a csv file passed as an argument and sends the data to visdom.
The data that is read and sent to visdom is
'''


import sys
import csv
import visdom
import numpy as np
import pandas

# Read the data FirstName,LastName,Email,PhoneNumber,Languages,Age,University,StudyProgram,BachelorMasterPHD,Semester,Motivation,Timestamp


def parse_csv_line(line):
    '''
    Reads the csv data using panas.
    '''
    df = pandas.read_csv(line)
    return df


def read_csv_file(file_name):
    '''
    Reads the csv data using pandas.
    '''
    df = pandas.read_csv(file_name)
    return df


def extract_data(df):
    '''
    Extracts the data from the data frame.
    '''
    FirstName = df['FirstName']
    LastName = df['LastName']
    Email = df['Email']
    PhoneNumber = df['PhoneNumber']
    Languages = df['Languages']
    Age = df['Age']
    University = df['University']
    StudyProgram = df['StudyProgram']
    BachelorMasterPHD = df['BachelorMasterPHD']
    Semester = df['Semester']
    Motivation = df['Motivation']
    Timestamp = df['Timestamp']
    return FirstName, LastName, Email, PhoneNumber, Languages, Age, University, StudyProgram, BachelorMasterPHD, Semester, Motivation, Timestamp


def create_visdom_connection():
    '''
    Creates a visdom connection.
    '''
    vis = visdom.Visdom()
    return vis

def show_all_data_as_text(vis, FirstName, LastName, Email, PhoneNumber, Languages, Age, University, StudyProgram, BachelorMasterPHD, Semester, Motivation, Timestamp):
    '''
    Shows all the data as text.
    '''

    # Check if win text exists and create it if it does not exist.
    for i in range(len(FirstName)):
        # Append to existing text data.
        if vis.win_exists('text'):
            vis.text(f'FirstName: {FirstName[0]}', win='text', append=True)
        else:
            vis.text(f'FirstName: {FirstName[0]}', win='text', opts=dict(title='text'))
        vis.text(f'LastName: {LastName[i]}', win='text', append=True)
        vis.text(f'Email: {Email[i]}', win='text', append=True)
        vis.text(f'PhoneNumber: {PhoneNumber[i]}', win='text', append=True)
        vis.text(f'Languages: {Languages[i]}', win='text', append=True)
        vis.text(f'Age: {Age[i]}', win='text', append=True)
        vis.text(f'University: {University[i]}', win='text', append=True)

def send_raw_csv_data_to_visdom(vis, file_name):
    '''
    Sends the raw csv data to visdom.
    '''
    df = read_csv_file(file_name)
    vis.text(df.to_string(), win='raw_data_as_text', opts=dict(title='raw_data_as_text'))


def send_visdom_test_message(vis):
    '''
    Test message.
    '''
    vis.text('Hello, world!', win='text_test')



def send_data_to_visdom(vis, FirstName, LastName, Email, PhoneNumber, Languages, Age, University, StudyProgram, BachelorMasterPHD, Semester, Motivation, Timestamp):
    '''
    Sends the data to visdom.
    '''
    show_all_data_as_text(vis, FirstName, LastName, Email, PhoneNumber, Languages, Age, University, StudyProgram, BachelorMasterPHD, Semester, Motivation, Timestamp)


def plot_the_ages(vis, df):
    '''
    Plots the ages as a bar plot.
    '''
    ages = df['Age']
    # get a dict with the age as the key and the num of people as the value.
    ages_dict = {}
    for age in ages:
        if age in ages_dict:
            ages_dict[age] += 1
        else:
            ages_dict[age] = 1
    # get the ages as a list.
    ages_list = [age for age in ages_dict]
    # get the age values as a list.
    age_values = [ages_dict[age] for age in ages_dict]
    # Create the bar plot with the age on X and the num as Y.
    vis.bar(X=age_values, opts=dict(rownames=ages_list))

    # Create a pie plot with the ages.
    vis.pie(X=age_values, opts=dict(legend=ages_list))

def main():
    '''
    Main function.
    '''
    # Read the data FirstName,LastName,Email,PhoneNumber,Languages,Age,

def main():
    '''
    Main function.
    '''
    # Read the data FirstName


def main():
    '''
    Main function.
    '''
    # Read the data FirstName,LastName,Email,PhoneNumber,Languages,Age,University,StudyProgram,BachelorMasterPHD,Semester,Motivation,Timestamp
    file_name = sys.argv[1]
    df = read_csv_file(file_name)
    # Extract the data
    FirstName, LastName, Email, PhoneNumber, Languages, Age, University, StudyProgram, BachelorMasterPHD, Semester, Motivation, Timestamp = extract_data(df)
    # Create a visdom connection
    vis = create_visdom_connection()
    plot_the_ages(vis, df)
    # Send test message to visdom.
    send_visdom_test_message(vis)
    # Send the data to visdom
    send_data_to_visdom(vis, FirstName, LastName, Email, PhoneNumber, Languages, Age, University, StudyProgram, BachelorMasterPHD, Semester, Motivation, Timestamp)


if __name__ == '__main__':
    main()

