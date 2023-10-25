from flask import Flask, render_template, request, url_for, flash, redirect
app = Flask(__name__)
from flask_login import login_required, current_user
from werkzeug.exceptions import abort, BadRequestKeyError
# for lock api, #FIXME change name of app, #FIXME use separate file
from flask_restful import Resource, Api  
api = Api(app)

import sqlite3
import os
import ldap
import datetime

# FIXME create app # https://stackoverflow.com/questions/15583671/flask-how-to-architect-the-project-with-multiple-apps
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login


app.config['SECRET_KEY'] = os.urandom(12)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))






''' A page used to add users
    It can be used a enrollment_id to add user to room_number
    After the request for adding, a message is displayed
    indicating success or error with its 'error type'
    'error type' can be one of {WrongUser, WrongRoom, AlreadyAdded, Unknown}
'''
@app.route('/users', methods=('GET', 'POST'))
def users():
    if request.method == 'POST':
        user_id = None
        room_id = None
        try:
            user_id = request.form['user_id']
            room_id = request.form['room_id']
        except:
            flash('Corrupted data sent!', 'alert_fail')
        
        if not room_id or not user_id:
            if not room_id:
                flash('Room ID is required!', 'alert_fail')
            if not user_id:
                flash('User ID is required!', 'alert_fail')
        else:
            flash('User and room added', 'alert_ok')
        

        if True:
            pass
        else:
            pass
            '''conn = get_db_connection()
            conn.execute('INSERT INTO main (room_id, user_id, succeded) VALUES (?, ?, ?)',
                         (title, content, 'TRUE'))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))'''
            flash('User added!', 'alert_ok')
    permissions = get_permissions_list()
    
    
    return render_template('users.html', permissions=permissions)

#FIXME dummy function for access local db
''' Get room list access from local DB 
    @return a row object, such as r['col1'],r['col2']... for r int row 
'''
def get_permissions_list():
    db_path = os.path.join(BASE_DIR, "database/permissions.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    q_res = conn.execute('SELECT * FROM permissions').fetchall()
    conn.close()
    return q_res

''' Get list of rooms included in LDAP server and exhibit them in a table
    Can include new rooms in LDAP server
'''
@app.route('/rooms', methods=('GET', 'POST'))
def rooms():
    if request.method == 'POST':
        room_id = None
        # room_name is got from ldap?
        try:
            room_id = request.form['room_id']
        except:
            flash('Corrupted data sent!', 'alert_fail')
       
        if not room_id:
            flash('Room ID is required!', 'alert_fail')
        else:
            flash('Room ID added!', 'alert_ok')
            '''conn = get_db_connection()
            conn.execute('INSERT INTO main (room_id, user_id, succeded) VALUES (?, ?, ?)',
                         (title, content, 'TRUE'))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))'''
    
    rooms = get_rooms()
    
    return render_template('rooms.html', rooms=rooms)

def get_rooms():
    db_path = os.path.join(BASE_DIR, "database/rooms.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    q_res = conn.execute('SELECT * FROM rooms').fetchall()
    conn.close()
    return q_res


''' Do logout from server
'''
@app.route('/logout', methods=('GET',))
def logout():
    flash('Logged out!', 'alert_ok')
    return redirect(url_for('login'))

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        flash('Logged in!', 'alert_ok')
        return redirect(url_for('index'))
    
    return render_template('login.html')

'''
'''
#TODO minimal api here https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
# once a class is defined, from Resource, you can add methods that are mapped to http methods
# using api.add_resource, its possible to add a class to it and any desired endpoint ie. api.add_resource(Todo, '/todos/<todo_id>')

class Lock_Api(Resource):
    def get(self):
        return {'hello': 'get'}
    def post(self):
        # TODO check if data is valid
        # consult db of permissions
        # respond with granted or denied
        return {'hello': 'post'}

api.add_resource(Lock_Api, '/api')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)



@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    flash('olaaaaaa')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            flash('nao tem update entradas no bd, apenas cresce')
            conn = get_db_connection()
            #conn.execute('UPDATE main SET title = ?, content = ?'
            #             ' WHERE id = ?',
            #             (title, content, id))
            #conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# ...

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))





