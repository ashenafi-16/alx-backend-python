import sqlite3
class ExecuteQuery:
    def __init__(self, db_name, query, param):
        self.db_name = db_name
        self.query = query
        self.param = param
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, (self.param,))
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
query = "SELECT * FROM users WHERE age > ?"
param = 25

with ExecuteQuery('users.db', query, param) as results:
    print("Users older than 25:")
    for user in results:
        print(user)