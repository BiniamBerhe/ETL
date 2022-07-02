from Utils import extract, transform, db_conn


path = '/home/biniam/Desktop/ETL_Pipline/Utils/resources/input-datasets'
if __name__ == "__main__":
    
    df = extract.json_to_df(path)
    df = extract.extract_countries(df)
    df = extract.extract_dates(df)
    df_daily_avg_value = transform.daily_avg_value(df)
    final_df = transform.aqi_calculator(df_daily_avg_value)
    print(db_conn.write_data(final_df))