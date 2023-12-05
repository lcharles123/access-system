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
    remember = request.form.get('remember') == True
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


