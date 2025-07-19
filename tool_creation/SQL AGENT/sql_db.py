import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='@Mysql123',
    database='chatbot'
)

cursor = connection.cursor()

# Create table (optional if already created)
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
"""
cursor.execute(table_info)

# Optional: clear previous data to avoid duplicates
cursor.execute("DELETE FROM STUDENT")

# Insert new records
records = [
    ('Muskan', 'Data Science', 'A', 90),
    ('Nitish', 'Data Science', 'B', 100),
    ('Sam', 'Data Science', 'A', 86),
    ('Alok', 'DEVOPS', 'A', 50),
    ('Ipshita', 'DEVOPS', 'A', 35)
]

cursor.executemany("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (%s, %s, %s, %s)", records)

# Display inserted records
print("The inserted records are:")
cursor.execute("SELECT * FROM STUDENT")
for row in cursor.fetchall():
    print(row)

# Commit and close
connection.commit()
cursor.close()
connection.close()
