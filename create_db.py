import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Drop the table if it exists (for clean recreation)
cursor.execute("DROP TABLE IF EXISTS admin")

# Create table with correct columns
cursor.execute("""
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Insert a test admin user
cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', '123456'))

conn.commit()
conn.close()
print("✅ Database and admin table created successfully!")