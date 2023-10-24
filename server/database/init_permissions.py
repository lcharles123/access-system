import sqlite3, sys


connection = sqlite3.connect('permissions.db')


with open('schema_permissions.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO permissions (room_id, user_id) VALUES (?, ?)",
            ('1111', 'ana')
            )

cur.execute("INSERT INTO permissions (room_id, user_id) VALUES (?, ?)",
            ('2222', 'joao')
            )


connection.commit()
connection.close()


