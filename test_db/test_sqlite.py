import sqlite3

# connect to a datatabase (or create it if it doesn't exist)
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

#create a table
cursor.execute('CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, value TEXT)')
cursor.execute('INSERT INTO test_table (value) VALUES ("Hello, SQLite!")')
conn.commit()

#query the database
cursor.execute('SELECT * FROM test_table')
print(cursor.fetchall())

conn.close()