#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """Custom context manager for handling SQLite database connections"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open the connection when entering the context
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection when exiting the context
        if self.conn:
            self.conn.close()
        # If exception occurs, propagate it (don’t suppress)
        return False


# Example usage: query users table
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
