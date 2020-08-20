import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'Milan', 'rias'),
    (3, 'Cheyenne', 'tree'),
    (4, 'Wyatt', 'powe'),
    (5, 'Ryan', 'lmas'),
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# To save the data
connection.commit()

# To close the connection
connection.close()
