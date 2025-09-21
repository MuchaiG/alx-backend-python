import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db="users.db"):
        self.query = query
        self.params = params if params else ()
        self.db = db
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        # Open connection + execute query
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result   # returned to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Returning False lets exceptions (if any) propagate
        return False


#### Usage Example
query = "SELECT * FROM users WHERE age > ?"
param = (25,)

with ExecuteQuery(query, param) as results:
    print(results)
