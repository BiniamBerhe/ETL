import pandas as pd
from datetime import *
import os


def json_to_df(path):
    """
    It takes a path to a directory of JSON files, reads them in, and writes them out to a single CSV
    file
    
    :param path: The path to the JSON files
    """
    json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.ndjson')]
    df = pd.DataFrame()

    for _, js in enumerate(json_files):
        with open(os.path.join(path, js), encoding='utf-8') as json_file:
            df = df.append([pd.read_json(json_file,lines=True)])
    
    #df.to_csv('data.csv', index=False, encoding='utf-8')
    return df

def extract_countries(df):
    """
    It takes a dataframe, drops some columns, filters the dataframe to only include the countries we
    want, and then extracts the date and time from the date column
    
    :param df: the dataframe to be filtered
    :return: A dataframe with the countries GB, FR, and NL.
    """
    df = df.drop(['coordinates', 'attribution',
                            'location', 'mobile', 'sourceType', 'averagingPeriod'], axis=1)
    return df.loc[df['country'].isin(['GB', 'FR', 'NL'])]

def extract_dates(df_countries):
    """
    It takes a dataframe with a column called 'date' that contains a list of dictionaries, each of which
    has a key called 'utc' that contains a string in the format 'YYYY-MM-DDTHH:MM:SS.ffffff+00:00'. 
    
    It returns a dataframe with two new columns, 'hours' and 'dates', that contain the time and date,
    respectively, of each row.
    
    :param df_countries: the dataframe containing the data for the countries
    :return: A dataframe with the dates and hours extracted from the date column.
    """
    #for utc_date in utc_dates:
    utc_dates = [date_dict['utc'] for date_dict in df_countries['date']]
    dates = []
    hours = []
    for utc_date in utc_dates:
        dt_time = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S.%f%z")
        dates.append(str(dt_time.date()))
        hours.append(str(dt_time.time()))

    df_countries = df_countries.assign(hours=hours)
    df_countries = df_countries.assign(dates=dates)
    df_countries = df_countries.drop('date', axis=1)
    return df_countries.sort_values(by='country')

