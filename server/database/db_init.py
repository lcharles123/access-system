import logging
from server.database import db
from server.models import User, Permissions
import bcrypt

''' There will be only one user at the begining
    and he can create more users.
'''

def create_admin_user():
    user = User.query.filter_by(username="admin", role="admin").first()
    if user is None:
        user = User(
            username="admin",
            name="admin"
            password="admin",
            email="admin@example.com",
            role="admin"
        )
        db.session.add(user)
        db.session.commit()
        logging.info("Admin was set.")
    else:
        logging.info("Admin already set.")

# To dev purposes, populate the model

def create_tree_normal_users():
    user1 = User.query.filter_by(username="maria", role='user').first()
    user2 = User.query.filter_by(username="jose", role='user').first()
    user3 = User.query.filter_by(username="ana", role='user').first()
    if (user1 and user2 and user3) is None:
        users = [User(username="maria", name="maria", password="maria123", email="maria@example.com"),
                 User(username="jose", name="jose", password="jose123", email="jose@example.com" ),
                 User(username="ana", name="ana", password="ana123", email="ana@example.com" )]
        for u in users:
            db.session.add(u)
        db.session.commit()
        logging.info("Three users was set.")
    else:
        logging.info("Three users was already set.")

def create_tree_locks():
    lock1 = User.query.filter_by(username="1111", name="WINET1", role='lock').first()
    lock2 = User.query.filter_by(username="2222", name="LAB1", role='lock').first()
    lock3 = User.query.filter_by(username="3333", name="LCC", role='lock').first()
    if (lock1 and lock2 and lock3) is None:
        locks = [User(username="1111", name="WINET1", role="lock"),
                 User(username="2222", name="LAB1", role="lock"),
                 User(username="3333", name="LCC", role="lock")]
        for u in locks:
            db.session.add(u)
        db.session.commit()
        logging.info("Three locks was set.")
    else:
        logging.info("Three locks was already set.")


def create_tree_permissions():
    p1 = Permissions.query.filter_by(room="1111", enrollment="2016065120").first()
    p2 = Permissions.query.filter_by(room="2222", enrollment="2016065120").first()
    p3 = Permissions.query.filter_by(room="2222", enrollment="2020064356").first()
    if (p1 and p2 and p3) is None:
        ps = [Permissions(room="1111", enrollment="2016065120"),
              Permissions(room="2222", enrollment="2016065120"),
              Permissions(room="2222", enrollment="2020064356")]
        for u in ps:
            db.session.add(u)
        db.session.commit()
        logging.info("Three permissions was set.")
    else:
        logging.info("Three permissions was already set.")


def create_tree_access():
    p1 = Entry_List.query.filter_by(room="1111", ).first()
    p2 = Entry_List.query.filter_by(username="2222", name="LAB1", role='lock').first()
    p3 = Entry_List.query.filter_by(username="3333", name="LCC", role='lock').first()
    if (p1 and p2 and p3) is None:
        locks = [Entry_List(username="1111", name="WINET1", role="lock"),
                 Entry_List(username="2222", name="LAB1", role="lock"),
                 Entry_List(username="3333", name="LCC", role="lock")]
        for u in locks:
            db.session.add(u)
        db.session.commit()
        logging.info("Three Entries was set.")
    else:
        logging.info("Three Entries was already set.")












