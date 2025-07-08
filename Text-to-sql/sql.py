import sqlite3 

connection = sqlite3.connect('student.db')

cursor = connection.cursor()

table_info = """
CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    grade TEXT,
    attendance_percentage REAL,
    pin TEXT
);
"""


cursor.execute(table_info)

##insert records

records = """
INSERT INTO student (name, age, grade, attendance_percentage, pin) VALUES
('Alice', 20, 'A', 85.5, '110001'),
('Bob', 21, 'B', 78.0, '110002'),
('Charlie', 22, 'A', 92.3, '110003'),
('David', 23, 'C', 65.8, '110004'),
('Eva', 20, 'B', 88.9, '110005'),
('Frank', 21, 'B', 74.5, '110006'),
('Grace', 22, 'A', 91.0, '110007'),
('Helen', 23, 'C', 69.2, '110008'),
('Ivy', 20, 'A', 95.7, '110009'),
('Jack', 21, 'B', 80.1, '110010');
"""

cursor.execute(records)

data = cursor.execute('select * from student')

for row in data:
    print(row)

connection.commit()
connection.close()