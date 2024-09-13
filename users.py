import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL)''')

# Insert sample credentials
users = [
    ('user', 'password'),
    ('rajat', 'rajat@123'),
    ('subhodeep', 'subhodeep@123'),
    ('mayuresh', 'mayuresh@123'),
    ('debajyoti', 'debajyoti@123')
]

for user in users:
    cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', user)

conn.commit()
conn.close()