import time
import sqlite3 
import functools


query_cache = {}

#### with_db_connection decorator (from earlier tasks)
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")   # open connection
        try:
            result = func(conn, *args, **kwargs) 
        finally:
            conn.close()   # always close connection
        return result
    return wrapper


#### cache_query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get query string (assume it's either in args[0] or kwargs["query"])
        query = None
        if args:
            query = args[0]
        elif "query" in kwargs:
            query = kwargs["query"]

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
