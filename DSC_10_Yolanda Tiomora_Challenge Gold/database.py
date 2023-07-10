import os
import sqlite3

def create_database_file(text):
    if not os.path.exists("hasil"):
        os.makedirs("hasil")
    conn = sqlite3.connect("hasil/hasil_teks.db")
    conn.execute("CREATE TABLE if not exists tweet(text VARCHAR)")
    conn.execute("INSERT INTO tweet VALUES (?)", (text,))
    conn.commit()
    conn.close()