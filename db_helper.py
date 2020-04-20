import datetime
import logging

# Will insert a row into the table with the corresponding rows and columns
def insert(connection, table_name, columns, values):
    cursor = connection.cursor()

    try:
        join_str = "', '"
        tick_str = "'"

        query = f"INSERT INTO {table_name}({', '.join(columns)}) VALUES({tick_str + join_str.join(values) + tick_str})"
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except Exception as e:
        logging.error(f'{str(datetime.datetime.now())}: Error inserting')
        logging.error(f'{str(datetime.datetime.now())}: {e}')
        cursor.close()

# Given a column and value, check if that row exists in the table
def does_exist(connection, table_name, column, value):
    cursor = connection.cursor()

    try:
        query = f"SELECT exists(SELECT * from {table_name} where {column} = '{value}')"
        cursor.execute(query)
        does_exist =  cursor.fetchone()[0]
        cursor.close()

        return does_exist
    except Exception as e:
        logging.error(f'{str(datetime.datetime.now())}: Error checking existence')
        logging.error(f'{str(datetime.datetime.now())}: {e}')
        cursor.close()

        return False

# Will remove a row base on column = value
def remove(connection, table_name, column, value):
    cursor = connection.cursor()

    try:
        query = f"DELETE FROM {table_name} where {column} = '{value}'"
        cursor.execute(query)
        connection.commit()
        cursor.close()
    except Exception as e:
        logging.error(f'{str(datetime.datetime.now())}: Error removing')
        logging.error(f'{str(datetime.datetime.now())}: {e}')
        cursor.close()

# Will return a list of tuples of all the rows in the corresponding table
def query_all(connection, table_name):
    cursor = connection.cursor()

    try:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result
    except Exception as e:
        logging.error(f'{str(datetime.datetime.now())}: Error querying all')
        logging.error(f'{str(datetime.datetime.now())}: {e}')
        cursor.close()

        return []
