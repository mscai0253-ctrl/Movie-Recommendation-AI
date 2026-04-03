import sqlite3

def connect_db():
    return sqlite3.connect("database/users.db")

def create_tables():
    conn = connect_db()
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS ratings (username TEXT, movie TEXT, rating INTEGER)")

    conn.commit()
    conn.close()

def add_user(u, p):
    conn = connect_db()
    conn.execute("INSERT INTO users VALUES (?,?)",(u,p))
    conn.commit()
    conn.close()

def login_user(u,p):
    conn = connect_db()
    data = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p)).fetchone()
    conn.close()
    return data