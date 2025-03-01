import sqlite3

# Connect to the database (or create it if it doesn’t exist)
conn = sqlite3.connect('certificates.db')

# Create a table for storing certificates (if not exists)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cert_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        issued_date TEXT NOT NULL
    )
''')

# Commit and close the database
conn.commit()
conn.close()

print("Database setup complete.")
