"""
Is used to manually add some trivial data for project testing.
Feel free to clear or delete customers_database since it is created every time app.py runs.
"""
import sqlite3

connection = sqlite3.connect('customers_database.db')
cursor = connection.cursor()

cursor.execute("INSERT INTO customers VALUES (4728695029, 'Ivanov', 'Ivan', 170521, 5431, 'silver')")
cursor.execute("INSERT INTO customers VALUES (3391860790, 'Nikita', 'Nikitov', 151001, 120, 'standard')")
cursor.execute("INSERT INTO customers VALUES (1923434986, 'Anna', 'Sergeeva', 170210, 1560, 'bronze')")
cursor.execute("INSERT INTO customers VALUES (2134235769, 'Alena', 'Smolova', 180512, 788, 'standard')")
cursor.execute("INSERT INTO customers VALUES (7534859233, 'Sergey', 'Potapov', 190202, 8235, 'silver')")
cursor.execute("INSERT INTO customers VALUES (8783942570, 'Artem', 'Shirkov', 170725, 11660, 'gold')")
cursor.execute("INSERT INTO customers VALUES (2375689540, 'Igor', 'Stoleshnikov', 180908, 5020, 'silver')")

connection.commit()
connection.close()
