import sqlite3
import ldap
from flask import Blueprint, current_app, render_template, request, url_for, flash, redirect, abort
from .database import db, db_init
from .database import operations as db_oper
from flask_login import login_required, current_user
from flask_restful import Resource, Api  
from .database.scheduled_operations import add_sched_entries, start_sched

from os import path

main = Blueprint('main', __name__)


''' Exhibit all accesses in the room system, need to be logged
    All accesses are stored in a local database
'''
# TODO can filter table by room, user, succeeded, date range

# FIXME sent to doing tests
@main.before_app_first_request
def create_tables():
    if not path.exists(current_app.config['SQLALCHEMY_DATABASE_URI']) or True:
        db.app = main
        db.drop_all()
        db.create_all()
        db_init.create_admin_user()
        db_init.create_tree_users()
        db_init.create_tree_locks()
        db_init.create_tree_lock_users()
        
        db_init.set_tree_permissions()
        db_init.create_tree_access()

''' Cleanup Enty_List after 6 months
    Clean permissions with expiration date, runs every day
'''
@main.before_app_first_request
def scheduler_jobs():
    sched = add_sched_entries()
    start_sched(sched)
    
''' List last access to locks.
'''
@main.route('/', methods=('GET', 'POST'))
#@login_required
def index():
    room = 'all'
    all_entry_table = db_oper.get_entry_table()
    filtered_entry_table = None
    if request.method == 'POST': # filter by room
        try:
            room = request.form['room']
        except:
            return abort(400)
    print('room', room)
    if room == 'all':
        filtered_entry_table = db_oper.get_entry_table()
    else:
        filtered_entry_table = db_oper.get_entry_table(on='room', element=room)
    
    #entry_table = db_oper.get_entry_table(on='room')
    #FIXME remove after implementing anothers
    perm = db_oper.get_permission_table()
    users = db_oper.get_all_table_users('user')
    admin = db_oper.get_all_table_users('admin')
    lock_users = db_oper.get_all_table_users('lock_user')
    locks = db_oper.get_all_table_users('lock')
    #print(len(entry_table), len(perm), len(users))
    #print(len(admin), len(lock_users), len(locks))
    #print(current_user.get_username)
    #print(entry_table[0].as_row)
    #for entry in entry_table:
    #    print(entry['room'])
    return render_template('index.html', current_user=current_user, 
                                        all_entry_table=all_entry_table,
                                        filtered_entry_table=filtered_entry_table) 
    

'''List all users, given a room number from a specific ldap server
'''
#TODO do a anon bind, receive credentials and return if bool if valid user
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

''' A page used to add or delete user permissions
    It can be used a enrollment_id to add user to room_number
    After the request for adding, a message is displayed
    indicating success or error of the operation
'''
@main.route('/users', methods=('GET', 'POST'))
#@login_required
def users():
    perm_list = db_oper.get_permission_table()
    if request.method == 'POST':
        user = None
        room = None
        filter_room = None
        room_to_delete = None
        user_to_delete = None
        try:
            filter_room = request.form['filter_room']
        except:
            pass
        try:
            room_to_delete = request.form['room_to_delete']
            user_to_delete = request.form['user_to_delete']
        except:
            pass
        try:
            user = request.form['user']
            room = request.form['room']
            print(user, room)
        except:   
            pass
        
        if filter_room is not None:
            if filter_room == 'all':
                pass # perm_list aready have all table
            else:
                perm_list = db_oper.get_permission_table(room=filter_room)
        elif room_to_delete is not None or user_to_delete is not None:
            if db_oper.revoke_permission(db, room_to_delete, user_to_delete):
                msg='Permissão do usuário "'+user_to_delete+'" à sala "'+room_to_delete+'" revogada.'
                flash(msg, 'alert_ok')
            else:
                msg='Erro ao revogar permissão, por favor selecione um usuário e uma sala.'
                flash(msg, 'alert_fail')
            perm_list = db_oper.get_permission_table() # update permissions after deleting
        elif room is not None or user is not None:
            if try_grant_permission(user, room) == True:
                msg = 'Usuário "'+user+'" adicionado à sala '+room+'.'
                flash(msg, 'alert_ok')
            perm_list = db_oper.get_permission_table() # update permissions after adding

    # for add permissions dropdown menu
    rooms = db_oper.get_all_table_users('lock')
    
    return render_template('users.html', rooms=rooms, permissions=perm_list) 

def try_grant_permission(user, room):
    if not db_oper.is_valid_user(room, 'lock'):
        flash('Sala invália, por favor, peça ao administrador do sistema para incluí-la.', 'alert_fail')
        return False
    #TODO validate user in LDAP here, if not valid, then
    #flash('Usuário não matriculado na instituição.', 'alert_fail') 
    #and return False
    #else if its valid, then check if its present in local db first:
    if not db_oper.is_valid_user(user, 'lock_user'):
        flash('Usuário "'+user+'" inválido.', 'alert_fail')
        return False
    #TODO else add to local database, because if its arrived here, then its already on LDAP
    if db_oper.check_permission(db, room, user):
        msg = 'Usuário "'+user+'" já possui a permissão para a sala "'+room+'".'
        flash(msg, 'alert_warn')
        return False # case have the permission
    elif db_oper.set_permission(db, room, user):
        return True
    else:
        flash('Erro ao adicionar usuário.', 'alert_fail') # motivo adverso
        return False

''' Get list of rooms included in LDAP server and exhibit them in a table
    Add rooms, only admin username '0' can add rooms
'''
@main.route('/rooms', methods=('GET', 'POST'))
#@login_required
def rooms():
    if request.method == 'POST':
        room = None
        name = None
        password = None
        room_to_del = None
        try:
            room_to_del = request.form['room_to_delete']
        except:
            pass
        try:
            room = request.form['room'] # username is the room number
            #TODO password = request.form['password']
            # seems not needed a password for add and check rooms
            password = '123'
            name = request.form['name']
        except:
            pass
        if room is not None or name is not None:
            if not room:
                flash('Por favor, forneça um Número de sala válido.', 'alert_fail')
            if not name:
                flash('Por favor, forneça um nome para a sala.', 'alert_fail')
            if db_oper.is_valid_user(room, 'lock'):
                flash('Sala "'+room+'" já existe.', 'alert_warn')
            if add_room(room, name):
                msg = 'Sala número "'+room+'" adicionada ao sistema.'
                flash(msg, 'alert_ok')
        elif room_to_del is not None:
            if db_oper.remove_user(db, room_to_del):
                flash('Sala "'+room_to_del+'" removida com sucesso.', 'alert_ok')
            else:
                flash('Erro ao remover: sala não cadastrada.', 'alert_fail')
    
    rooms = db_oper.get_all_table_users('lock')
    return render_template('rooms.html', rooms=rooms)

def add_room(room, name):
    if db_oper.insert_user(db, 'lock', 
                           atributes={'username': room, 
                           'password': '123', 
                           'name': name, 
                           'role': 'lock'}):
        return True
    else:
        flash('Erro ao adicionar sala.', 'alert_fail')
        return False

@main.route('/help')
def help():
    return render_template('help.html')

