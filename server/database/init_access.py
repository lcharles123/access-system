import sqlite3, sys

# temp db for access count register
# every time a access is granted or not, this db will be updated, for control purposes

connection = sqlite3.connect('access.db')
# access_count(*id, room_id, user_id, time, succeded)
with open('schema_access.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO access_count (room_id, user_id, granted) VALUES (?, ?, ?)",
            ('1111', 'ana', 'TRUE')
            )
cur.execute("INSERT INTO access_count (room_id, user_id, granted) VALUES (?, ?, ?)",
            ('2222', 'joao', 'TRUE')
            )
cur.execute("INSERT INTO access_count (room_id, user_id, granted) VALUES (?, ?, ?)",
            ('3333', 'maria', 'FALSE')
            )
#posts = connection.execute('SELECT * FROM room_users').fetchall()
#print(posts)
connection.commit()
connection.close()


