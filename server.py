from flask import Flask, request, jsonify, send_file
import sqlite3
app = Flask(__name__)

DATABASE = 'database.db'


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   log_date TEXT NOT NULL
    )
''')
    conn.commit()
    conn.close()


@app.route('/', methods=['GET'])
def get_items():
    print(request.json)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return jsonify(items)


@app.route('/', methods=['POST'])
def add_items():

    print(request.json)

    if not request.json:
        return jsonify({'error': 'Bad Request - No JSON data received'}), 400

    data = request.json

    if 'log_date' not in data:
        return jsonify({'error': 'Bad Request'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO items (log_date) VALUES (?)', (data['log_date'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item Added', 'log_date': data}), 200


if __name__ == '__main__':
    create_table()
    app.run(debug=True, port=8001)
