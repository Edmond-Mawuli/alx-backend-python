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

        while True:  # loop 1
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch   # ✅ return batches using yield

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Generator that yields users over 25 years old
    """
    for batch in stream_users_in_batches(batch_size):   # loop 2
        for user in batch:                             # loop 3
            if user['age'] > 25:
                yield user   # ✅ yield instead of print
