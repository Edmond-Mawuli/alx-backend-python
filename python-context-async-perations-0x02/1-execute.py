#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    """Context manager to execute a query and return results"""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open connection and execute query
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        # Always close connection
        if self.conn:
            self.conn.close()
        return False  # don’t suppress exceptions


# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery("users.db", query, (25,)) as results:
        print(results)
