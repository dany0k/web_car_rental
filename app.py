import sqlite3

from flask import Flask, render_template, abort

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('./db/carrental.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_client(post_id):
    conn = get_db_connection()
    client = conn.execute('SELECT * FROM client WHERE client_id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if client is None:
        abort(404)
    return client


@app.route('/<int:post_id>')
def client(post_id):
    client = get_client(post_id)
    return render_template('post.html', post=client)


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM client').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)
