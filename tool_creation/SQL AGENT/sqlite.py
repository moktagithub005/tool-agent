import sqlite3

# Connect or create the database
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE STUDENT (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    branch TEXT,
    grade TEXT,
    marks INTEGER
)
""")

# Insert sample data
students = [
    ("Ajay", "Physics", "A", 91),
    ("Neha", "CSE", "B", 75),
    ("Rahul", "ECE", "C", 60),
    ("Sneha", "Maths", "A", 88),
    ("Vikram", "Civil", "B", 70)
]

cursor.executemany("INSERT INTO STUDENT (name, branch, grade, marks) VALUES (?, ?, ?, ?)", students)
conn.commit()
conn.close()
