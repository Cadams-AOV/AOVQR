import sqlite3

# Connect to the database
conn = sqlite3.connect('certificates.db')
cursor = conn.cursor()

# Insert a test certificate (Change values if needed)
cursor.execute('''
    INSERT INTO certificates (cert_code, name, issued_date)
    VALUES (?, ?, ?)
''', ("TEST12345", "John Doe", "2025-03-01"))

# Commit changes & close
conn.commit()
conn.close()

print("Test certificate added.")
