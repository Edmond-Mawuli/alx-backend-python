#!/usr/bin/python3
import seed

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:   # 1st loop
        yield row["age"]

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Compute the average age using the generator without loading
    the entire dataset into memory
    """
    total = 0
    count = 0
    
    for age in stream_user_ages():   # 2nd loop
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
