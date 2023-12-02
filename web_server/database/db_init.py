import logging
from . import db
from .operations import *
from .models import *


def create_admin_user():
    atributes={'username': '0', 
               'email': 'admin@example.com', 
               'password':'123', 
               'role': 'admin'}
    r = insert_user(db, 'admin', atributes=atributes)
    if r:
        logging.info("Admin was set.")
    else:
        logging.info("Admin already set.")


# To dev purposes, populate the model
def create_tree_users(): 
    rs = []
    for name in ["andre", "roberto", "antonia"]:
        atributes={'username': str(sum(ord(c) for c in name) % 998 + 1), 
                   'name': name, 
                   'email': name+'@example.com', 
                   'password': name+'123', 
                   'role': 'user'}
        rs.append(insert_user(db, 'user', atributes=atributes))
    logging.info(str(rs))

def create_tree_locks(): 
    rs = []
    for num,name in [("1111","WINET1"),("2222","LAB1"),("3333","LCC")]:
        atributes={'name': name,
                   'username': num, 
                   'password': name+'123', 
                   'role': 'lock'}
        rs.append(insert_user(db, 'lock', atributes=atributes))
    logging.info(str(rs))

def create_tree_lock_users(): 
    rs = []
    for num,name in [("2020001234","maria"),("2020001236","jose"),("2020001235","ana")]:
        atributes={'name': name,
                   'username': num, 
                   'password': name+'123',
                   'email': name+"@example.com",
                   'role': 'lock_user'}
        rs.append(insert_user(db, 'lock_user', atributes=atributes))
    logging.info(str(rs))

def set_tree_permissions(): 
    rs = []
    for user,room in [("2020001234","1111"),("2020001234","2222"),("2020001235","2222")]:
        rs.append(set_permission(db, room, user))
    logging.info(str(rs))

def create_tree_access():
    rs = []
    for user,room in [("2020001234","1111"),("2020001234","2222"),("2020001236","3333")]:
        success = check_permission(db, room, user)
        rs.append(insert_entry_list(db, room, user, success))
    logging.info(str(rs))


