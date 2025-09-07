#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator function that streams rows from user_data table
    one by one as dictionaries
    """
    connection = None
    cursor = None
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # adjust if using another user
            password="yourpassword", 
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)  # fetch rows as dicts
        cursor.execute("SELECT * FROM user_data;")

        # Yield rows one by one
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
