import logging
import sqlite3


def create_table():
    try:
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            user_id INTEGER, 
            name TEXT,
            subject TEXT,
            level TEXT,
            task TEXT,
            answer TEXT);
        ''')
        logging.info("Create table.")
    except sqlite3.Error as error:
        logging.error("Error database:", error)
    finally:
        con.close()


def get_data():
    user = {}
    try:
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        query = cur.execute('''
            SELECT user_id, name, subject, level
            FROM users
            LIMIT 1
            ''')

        res = query.fetchall()
        user['user_id'] = res[0][0]
        user['name'] = res[0][1]
        user['subject'] = res[0][2]
        user['level'] = res[0][3]
        logging.info('get data from database')
    except sqlite3.Error as error:
        logging.error('Error database:', error)
    finally:
        con.close()
        return user


def insert_data(user_id=None, name=None, subject=None, level=None, task=None, answer=None):
    try:
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute(f'INSERT INTO users(user_id, name, subject, level, task, answer)'
                    f'VALUES (?, ?, ?, ?, ?, ?);',
                    (user_id, name, subject, level, task, answer))
        con.commit()
        logging.info('data is written to the database')
    except sqlite3.Error as error:
        logging.error('Error database:', error)
    finally:
        con.close()


def update_data(user_id, column, value):
    try:
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute(f'UPDATE users '
                    f'SET {column} = ? '
                    f'WHERE user_id = ?;', (value, user_id))
        con.commit()
        logging.info('data has been updated')
    except sqlite3.Error as error:
        logging.error('Error database:', error)
    finally:
        con.close()


def delete_data(user_id):
    try:
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        cur.execute(f'DELETE FROM users WHERE user_id = ?', (user_id,))
        con.commit()
        logging.info('data has been deleted from table')
    except sqlite3.Error as error:
        logging.error('Error database:', error)
    finally:
        con.close()
