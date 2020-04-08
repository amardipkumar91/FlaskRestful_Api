import sqlite3


connection = sqlite3.connect('data.db')


cursor = connection.cursor()

create_table = "create table users(id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'vicky', '123456')
insert_query = 'insert into users values (?, ?, ?)'
cursor.execute(insert_query, user)

select_query = 'select id from users'
all_data = cursor.execute(select_query)
for i in all_data:
    print (i)

connection.commit()
connection.close()