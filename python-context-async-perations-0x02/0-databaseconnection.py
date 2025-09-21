import sqlite3

class DatabaseConnection:
    def __init__(self, db="users.db"):
        self.db = db
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        return self.cursor   # gives direct access to cursor in 'with' block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Returning False propagates exceptions if they occur
        return False


#### Usage Example
with DatabaseConnection("users.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
