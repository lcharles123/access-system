from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user
main = Blueprint('main', __name__)


''' Exhibit all accesses in the room system, need to be logged
    All accesses are stored in a local database
'''
# TODO can filter table by room, user, succeeded, date range

@main.route('/')
@login_required
def index():
    rows = get_accesses()
    return render_template('index.html', rows=rows) 

''' Get user list access from local DB 
    @return a row object, such as r['col1'],r['col2']... for r int row 
'''
def get_accesses():
    db_path = os.path.join(BASE_DIR, "database/access.db")
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

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


