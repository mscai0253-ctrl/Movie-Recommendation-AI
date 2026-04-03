import sqlite3

def connect_db():
    return sqlite3.connect("database/users.db")

def save_rating(u,m,r):
    conn = connect_db()
    conn.execute("INSERT INTO ratings VALUES (?,?,?)",(u,m,r))
    conn.commit()
    conn.close()

def get_user_ratings(u):
    conn = connect_db()
    data = conn.execute("SELECT movie,rating FROM ratings WHERE username=?", (u,)).fetchall()
    conn.close()
    return data