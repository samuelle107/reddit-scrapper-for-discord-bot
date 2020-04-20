import datetime
import logging

# Will insert a row into the table with the corresponding rows and columns
def insert(connection, table_name, columns, values):
    try:
        join_str = "', '"
        tick_str = "'"

        cursor = connection.cursor()
        query = f"INSERT INTO {table_name}({', '.join(columns)}) VALUES({tick_str + join_str.join(values) + tick_str})"
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except:
        logging.error(f'{str(datetime.datetime.now())}: Error inserting')

# Given a column and value, check if that row exists in the table
def does_exist(connection, table_name, column, value):
    try:
        cursor = connection.cursor()
        query = f"SELECT exists(SELECT * from {table_name} where {column} = '{value}')"
        cursor.execute(query)
        does_exist =  cursor.fetchone()[0]
        cursor.close()
        return does_exist
    except:
        logging.error(f'{str(datetime.datetime.now())}: Error checking existence')
        return False

# Will remove a row base on column = value
def remove(connection, table_name, column, value):
    try:
        cursor = connection.cursor()
        query = f"DELETE FROM {table_name} where {column} = '{value}'"
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except:
        logging.error(f'{str(datetime.datetime.now())}: Error removing')

# Will return a list of tuples of all the rows in the corresponding table
def query_all(connection, table_name):
    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result
    except:
        logging.error(f'{str(datetime.datetime.now())}: Error querying all')
        return []
