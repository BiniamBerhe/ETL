import sqlite3 as db

def write_data(df):
    """
    It takes a dataframe as input, connects to the database, writes the dataframe to the database, and
    closes the connection.
    
    :param df: The dataframe that you want to write to the database
    :return: a string.
    """
    conn = db.connect('sqlite.db')
    df.to_sql('Air_quality', conn, if_exists='replace')
    conn.close()

    return 'Data inserted successfully'

    