from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    data = None
    if request.method == 'POST':
        id_ = '.'.join([request.form['num1'], request.form['num2'], request.form['num3']])
        conn = sqlite3.connect('sqlite.db')  # Change this to your SQLite DB path
        c = conn.cursor()
        c.execute('SELECT * FROM entries WHERE id=?', (id_,))
        row = c.fetchone()
        if row is not None:
            data = {
                'id': row[0],
                'description': row[1],
                'pass': row[2],
                'fail': row[3],
                'skip': row[4]
            }
        conn.close()
    return render_template('home.html', data=data)


def get_row(id_):
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute('SELECT * FROM entries WHERE id=?', (id_,))
    row = c.fetchone()
    conn.close()
    if row is not None:
        return {
            'id': row[0],
            'description': row[1],
            'pass': row[2],
            'fail': row[3],
            'skip': row[4]
        }


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    data = None
    if request.method == 'POST':
        id_ = '.'.join([request.form['num1'], request.form['num2'], request.form['num3']])
    else:  # It's a GET request
        id_ = request.args.get('id')
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()
    c.execute('SELECT * FROM entries WHERE id=?', (id_,))
    row = c.fetchone()
    if row is not None:
        data = {
            'id': row[0],
            'description': row[1],
            'pass': row[2],
            'fail': row[3],
            'skip': row[4]
        }
    conn.close()
    return render_template('edit.html', data=data)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search query
    conn = sqlite3.connect('sqlite.db')
    c = conn.cursor()

    # Execute the SQL query (be careful to avoid SQL injection!)
    c.execute("SELECT * FROM entries WHERE description LIKE ?", ('%' + query + '%',))

    rows = c.fetchall()
    results = [{'id': row[0], 'description': row[1], 'pass': row[2], 'fail': row[3], 'skip': row[4]} for row in rows]
    conn.close()
    return render_template('search.html', results=results)


if __name__ == '__main__':
    app.run(host="10.1.10.116", debug=True)
