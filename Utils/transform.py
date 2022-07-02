import pandas as pd
from datetime import *
import json
import os
import aqi


def daily_avg_value(df):
    """
    It takes a dataframe, groups it by city, country, parameter, sourceName, dates, and unit, and then
    calculates the mean value for each group
    
    :param df: the dataframe
    :return: A dataframe with the average value of each parameter for each day.
    """
    grouped = df.groupby(['city', 'country', 'parameter', 'sourceName', 'dates', 'unit'])['value'].mean().reset_index()
    return grouped.sort_values(by=['country'])

def aqi_calculator(daily_avg_value):

    pm25_value = daily_avg_value.query('parameter == "pm25" & value > 0')
    pm25 = list()
    for x in pm25_value['value']:
        value = aqi.to_iaqi(aqi.POLLUTANT_PM25, x, algo=aqi.ALGO_EPA)
        pm25.append(get_aqi_category(value))
    aqi_pm25 = pm25_value.assign(pm25_aqi = pm25)
    
    pm10_value = daily_avg_value.query('parameter == "pm10" & value > 0')
    pm10 = list()

    for x in pm10_value['value']:
        value = aqi.to_iaqi(aqi.POLLUTANT_PM10, x, algo=aqi.ALGO_EPA)
        pm10.append(get_aqi_category(value))
    aqi_pm10 = pm10_value.assign(pm10_aqi = pm10)

    aqi_category = pd.concat([aqi_pm25,aqi_pm10]).fillna('None')
    transformed_df = pd.concat([aqi_category,daily_avg_value], ignore_index=True).drop_duplicates(subset='value').fillna('No')
    return transformed_df


def get_aqi_category(x):
    if x <= 50:
        return "Good"
    elif x <= 100:
        return "Moderate"
    elif x <= 150:
        return "Unhealthy for Sensitive Groups"
    elif x <= 200:
        return "Unhealthy"
    elif x <= 300:
        return "Very Unhealthy"
    elif x > 300:
        return "Hazardous"
    else:
        return None
