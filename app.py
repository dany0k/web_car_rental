import sqlite3

from flask import Flask, render_template, abort, request, flash, redirect, url_for

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
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        violation = request.form['violation']

        print(firstname, surname, violation)

        if not firstname or not surname or not violation:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO client (firstname, surname, violation) VALUES (?, ?, ?)',
                         (firstname, surname, violation))
            conn.commit()
            conn.close()
            # return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:client_id>/edit', methods=('GET', 'POST'))
def edit(client_id):
    cur_client = get_client(client_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        violation = request.form['violation']

        if not firstname or not surname or not violation:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE client SET firstname = ?, surname = ?, violation = ?'
                         ' WHERE client_id = ?',
                         (firstname, surname, violation, client_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=cur_client)


@app.route('/<int:client_id>/delete', methods=('POST',))
def delete(client_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM client WHERE client_id = ?', (client_id,))
    conn.commit()
    conn.close()
    flash('Client was successfully deleted!')
    return redirect(url_for('index'))


@app.route('/')
def index():
    conn = get_db_connection()
    cur_client = conn.execute('SELECT * FROM client').fetchall()
    conn.close()
    return render_template('index.html', posts=cur_client)
