import sqlite3
import ldap
from flask import Blueprint, current_app, render_template, request, url_for, flash, redirect
from server.database import db, db_init
from server.database import operations as db_oper
from flask_login import login_required, current_user
from flask_restful import Resource, Api  
from os import path


#FIXME remove after factoration
BASE_DIR = path.dirname(path.abspath(__file__))
main = Blueprint('main', __name__)


''' Exhibit all accesses in the room system, need to be logged
    All accesses are stored in a local database
'''
# TODO can filter table by room, user, succeeded, date range

@main.before_app_first_request
def create_tables():
    if not path.exists(current_app.config['SQLALCHEMY_DATABASE_URI']):
        db.app = main
        db.drop_all()
        db.create_all()
        db_init.create_admin_user()
        db_init.create_tree_users()
        db_init.create_tree_locks()
        db_init.create_tree_lock_users()
        db_init.set_tree_permissions()
        db_init.create_tree_access()

''' List last access to locks.
'''
@main.route('/')
#@login_required
def index():
    rows = db_oper.get_entry_table()
    #print(rows[0].as_row)
    return render_template('index.html', current_user=current_user, rows=rows) 
    

'''List all users, given a room number from a specific ldap server
'''
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
        user = None
        room = None
        try:
            user = request.form['user']
            room = request.form['room']
        except:
            flash('Dados corrompidos!', 'alert_fail')
        
        if not user or not room:
            if not room:
                flash('Ientificador da sala em branco!', 'alert_fail')
            if not user:
                flash('Identificador de usuário em branco!', 'alert_fail')
            
#       elif  TODO validate user in LDAP here, if not valid, then
#           flash('Usuario nao matriculado na instituicao.', 'alert_fail')          
            
        else:
        
            if not db_oper.is_valid_user(db, user, 'user') or
                not db_oper.is_valid_user(db, user, 'lock_user'):
                flash('Usuário '+user+' não e válido.', 'alert_fail') 
            if not db_oper.is_valid_user(db, room, 'lock'):
                flash('Fechadura número '+user+' não e válida.', 'alert_fail') 
            # user validatede here, check permission
            if db_oper.check_permission(room, user):
                msg = 'Usuário '+user+' já possui a permissão para a sala '+room
                flash(msg, 'alert_warn')
            elif db_oper.set_permission(room, user):
                msg = 'Usuário '+user+' adicionado à sala '+room+'.'
                flash(msg, 'alert_ok')
            else:
                flash('Erro ao adicionar usuário.', 'alert_fail')
                
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
            
            flash('Sala Inexistente, por favor cadasatre-a ***aqui***', 'alert_fail')
    permissions = db_oper.get_permission_table()
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


@main.route('/help')
def help():
    return render_template('help.html')


