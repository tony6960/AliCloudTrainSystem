import sqlite3


def create_conn():
    return sqlite3.connect('ats.db', check_same_thread=False)


def create_cursor(conn):
    return conn.cursor()


def create_conn_cursor():
    conn = create_conn()
    cursor = create_cursor(conn)
    return cursor
