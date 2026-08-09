# build_db.py
import sqlite3

conn = sqlite3.connect("library.db")
conn.executescript(open("schema.sql").read())
conn.commit()
conn.close()
print("Database built successfully.")