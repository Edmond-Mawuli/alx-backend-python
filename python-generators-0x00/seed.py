#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

# 1. Connect to the MySQL server (no database yet)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # change if your MySQL uses a different user
            password="root"       # update with your actual password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create database ALX_prodev if it does not exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created successfully (or already exists)")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

# 3. Connect directly to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 4. Create user_data table if it does not exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            )
        """)
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# 5. Insert data into user_data from a CSV file
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Avoid duplicates by checking email
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
        connection.commit()
        cursor.close()
        print("Data inserted successfully from CSV")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
