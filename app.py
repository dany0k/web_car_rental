import sqlite3

from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

def get_db_connection():
    conn = sqlite3.connect('./db/carrental.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_client(client_id):
    conn = get_db_connection()
    client = conn.execute('SELECT * FROM client WHERE client_id=?',
                        (client_id,)).fetchone()
    conn.close()
    if client is None:
        abort(404)
    return client


@app.route('/<int:client_id>')
def client(client_id):
    cur_client = get_client(client_id)
    return render_template('client.html', post=cur_client)


@app.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('create.html')


@app.route('/')
def index():
    conn = get_db_connection()
    cur_client = conn.execute('SELECT * FROM client').fetchall()
    conn.close()
    return render_template('index.html', posts=cur_client)
