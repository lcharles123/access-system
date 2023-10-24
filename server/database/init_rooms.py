import sqlite3, sys

# list of rooms, not necessarily need to get rooms from ldap, 
# the department will have to enter them here manually
# or from a list

connection = sqlite3.connect('rooms.db')
# main(*id, room_id, user_id, time, succeded)
with open('schema_rooms.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO rooms (room_id, room_name) VALUES (?, ?)",
            ('1111', 'Lab 1')
            )
            
cur.execute("INSERT INTO rooms (room_id, room_name) VALUES (?, ?)",
            ('2222', 'Room 1')
            )
cur.execute("INSERT INTO rooms (room_id, room_name) VALUES (?, ?)",
            ('3333', 'Lab 2')
            )
connection.commit()
connection.close()


