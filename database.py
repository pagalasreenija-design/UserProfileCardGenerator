import sqlite3

conn = sqlite3.connect("profiles.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    bio TEXT,
    image TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")