#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from user_data
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # adjust if using another user
            password="yourpassword",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # yield the entire batch as a list of rows

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches, filtering only users older than 25
    """
    for batch in stream_users_in_batches(batch_size):   # loop 1
        for user in batch:                             # loop 2
            if user['age'] > 25:                       # filtering
                yield user
