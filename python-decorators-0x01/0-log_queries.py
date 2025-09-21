import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # extract query argument
        query = None
        if args:   # check positional args
            query = args[0]
        elif "query" in kwargs:  # check keyword arg
            query = kwargs["query"]

        if query:
            print(f"[LOG] Executing SQL query: {query}")
        else:
            print("[LOG] No query provided")

        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
