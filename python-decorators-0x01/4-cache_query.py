import sqlite3
import time
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract query from args or kwargs
        if 'query' in kwargs:
            query_str = kwargs['query']
        elif len(args) > 0:
            query_str = args[0]
        else:
            raise ValueError("No SQL query found.")

        # Check cache
        if query_str in query_cache:
            print("🔁 Returning cached result for query.")
            return query_cache[query_str]

        # Not in cache, call the function
        print("📥 Executing and caching query.")
        result = func(conn, *args, **kwargs)
        query_cache[query_str] = result
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