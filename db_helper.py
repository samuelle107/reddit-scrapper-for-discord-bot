# Will insert a row into the table with the corresponding rows and columns
def insert(connection, table_name, columns, values):
    join_str = "', '"
    tick_str = "'"

    cursor = connection.cursor()
    query = f"INSERT INTO {table_name}({', '.join(columns)}) VALUES({tick_str + join_str.join(values) + tick_str})"
    cursor.execute(query)
    connection.commit()
    cursor.close()

# Given a column and value, check if that row exists in the table
def does_exist(connection, table_name, column, value):
    cursor = connection.cursor()
    query = f"SELECT exists(SELECT * from {table_name} where {column} = '{value}')"
    cursor.execute(query)
    does_exist =  cursor.fetchone()[0]
    cursor.close()
    return does_exist

# Will remove a row base on column = value
def remove(connection, table_name, column, value):
    cursor = connection.cursor()
    query = f"DELETE FROM {table_name} where {column} = '{value}'"
    cursor.execute(query)
    connection.commit()
    cursor.close()

# Will return a list of tuples of all the rows in the corresponding table
def query_all(connection, table_name):
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    return result
