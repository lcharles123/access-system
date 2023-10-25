import sqlite3
import ldap
from flask import Blueprint, render_template, request, url_for, flash, redirect
from . import db
from flask_login import login_required, current_user
from flask_restful import Resource, Api  
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))
main = Blueprint('main', __name__)
api = Api(main)

''' Exhibit all accesses in the room system, need to be logged
    All accesses are stored in a local database
'''
# TODO can filter table by room, user, succeeded, date range

@main.route('/')
#@login_required
def index():
    rows = get_accesses()
    return render_template('index.html', current_user=current_user, rows=rows) 

''' Get user list access from local DB 
    @return a row object, such as r['col1'],r['col2']... for r int row 
'''
def get_accesses():
    db_path = path.join(BASE_DIR, "database/access.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    q_res = conn.execute('SELECT * FROM access_count').fetchall()
    conn.close()
    return q_res
    

'''List all users, given a room number from a specific ldap server'''
def list_users(room_number, url='ldap://serv.hopto.org', admin='cn=admin,dc=ufmg,dc=br', pwd='yweruyoityutrwgfjdytuasdfrtasf'):
    ldap_srv = ldap.initialize(url)
    ldap_srv.protocol_version = ldap.VERSION3
    ldap_srv.set_option(ldap.OPT_REFERRALS, 0)
    ldap_srv.simple_bind_s(admin, pwd)
    
    base = "cn="+str(room_number)+",ou=rooms,dc=ufmg,dc=br"
    criteria = "(objectClass=posixGroup)" # list all users
    attributes = ['memberUid']
    try:
        users = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)[0][1]['memberUid']
    except:
        users = [b'']
    if users[0] == b'':
        return b''   
    users = [str(i).replace(',', '=').split('=')[1] for i in users]
    ldap_srv.unbind()
    return users


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM main WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

''' A page used to add users
    It can be used a enrollment_id to add user to room_number
    After the request for adding, a message is displayed
    indicating success or error with its 'error type'
    'error type' can be one of {WrongUser, WrongRoom, AlreadyAdded, Unknown}
'''
#TODO adicionar data de término automático da permissão
@main.route('/users', methods=('GET', 'POST'))
#@login_required
def users():
    if request.method == 'POST':
        user_id = None
        room_id = None
        try:
            user_id = request.form['user_id']
            room_id = request.form['room_id']
        except:
            flash('Dados corrompidos!', 'alert_fail')
        
        if not room_id or not user_id:
            if not room_id:
                flash('Ientificador da sala em branco!', 'alert_fail')
            if not user_id:
                flash('Identificador de usuário em branco!', 'alert_fail')
        else:
            msg = 'Usuário '+''+' adicionado à sala '+''
            flash(msg, 'alert_ok')
        

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
            flash('Matrícula de usuário inexistente!', 'alert_fail')
            flash('Sala Inexistente, por favor cadasatre-a ***aqui***', 'alert_fail')
    permissions = get_permissions_list()
    
    
    return render_template('users.html', permissions=permissions)

#FIXME dummy function for access local db
''' Get room list access from local DB 
    @return a row object, such as r['col1'],r['col2']... for r int row 
'''
def get_permissions_list():
    db_path = path.join(BASE_DIR, "database/permissions.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    q_res = conn.execute('SELECT * FROM permissions').fetchall()
    conn.close()
    return q_res

''' Get list of rooms included in LDAP server and exhibit them in a table
    Can include new rooms in LDAP server
'''
@main.route('/rooms', methods=('GET', 'POST'))
#@login_required
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
    db_path = path.join(BASE_DIR, "database/rooms.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    q_res = conn.execute('SELECT * FROM rooms').fetchall()
    conn.close()
    return q_res

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

@main.route('/help')
def help():
    return render_template('help.html')


