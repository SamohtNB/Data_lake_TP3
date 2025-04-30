import mysql.connector
# Connect to MySQL database

conn = mysql.connector.connect(
    host = "localhost" ,
    user = "root" ,
    password = "root" ,
    database = "staging"
)
cursor = conn.cursor()
# Check data
cursor.execute('SELECT * FROM texts WHERE text IS NOT NULL')
count = cursor.fetchone()
print(f"number of valid rows : {count[0]}")

cursor.fetchall()

cursor.close()
conn.close()
