import sqlite3


def CreateDB():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    username TEXT,
    form INTEGER,
    rating INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions(
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    question TEXT,
    create_date TEXT
    )
    ''')
    connection.commit()
    connection.close()