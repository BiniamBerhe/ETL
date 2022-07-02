import sqlite3 as db
import pandas as pd

def load_data():
    """
    It connects to the database, executes a query, and returns the results as a pandas dataframe
    :return: A string
    """
    conn = db.connect('sqlite.db')
    dff = pd.read_sql_query('select * from Air_quality where city == "Paris"', conn)
    print(dff)
    conn.close()

    return 'Data inserted successfully'
load_data()