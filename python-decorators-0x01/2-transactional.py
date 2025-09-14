#!/usr/bin/env python3
import sqlite3
import functools


def with_db_connection(func):
    """Decorator to open and close a database connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # open connection
        try:
            result = func(conn, *args, **kwargs)  # pass connection to function
        finally:
            conn.close()  # always close connection
        return result
    return wrapper


def transactional(func):
    """Decorator to manage database transactions (commit or rollback)"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()   # commit if successful
            return result
        except Exception as e:
            conn.rollback()  # rollback on error
            raise e
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Example usage
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("User email updated successfully!")
