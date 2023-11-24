from flask import Blueprint, render_template, redirect, url_for, request, flash
from bcrypt import hashpw, checkpw
from .database.models import User
from flask_login import login_user, login_required, logout_user
from .database import db


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')
    
@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = None
    if username in ['admin', '0']:
        user = User.query.filter_by(username='0', role='admin').first()
    else:
        user = User.query.filter_by(username=username).first()
        if user and user.role != 'user':
            flash('Usuário não autorizado.', 'alert_fail')
            return redirect(url_for('auth.login'))
    
    if not user or not checkpw((password).encode(), user.password):
        flash('Usuário ou senha incorretos, por favor, tente novamente.', 'alert_fail')
        return redirect(url_for('auth.login')) 
    login_user(user, remember=remember)
    flash('Sucesso ao logar-se', 'alert_ok')
    return redirect(url_for('main.index'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    






# FIXME there is no signup here, the system will have a admin user and he can add or remove users, this page will be for him , use this to create users
'''@auth.route('/signup')
def signup():
    return render_template('signup.html')
@auth.route('/signup', methods=['POST'])'''
#def signup_post():
def add_user():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists', 'alert_fail')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


