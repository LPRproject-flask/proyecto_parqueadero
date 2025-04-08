import sqlite3

conn = sqlite3.connect("db/data.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(plates);")
for col in cursor.fetchall():
    print(col)
conn.close()

