from flask import Flask, render_template, request, url_for, flash, redirect
app = Flask(__name__)
from flask_login import login_required, current_user
from werkzeug.exceptions import abort, BadRequestKeyError
from flask_restful import Resource, Api  
api = Api(app)

import sqlite3
import os

import datetime





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





