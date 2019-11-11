import sqlite3
from flask import g

DATABASE = 'ldap.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        sqlite3.enable_callback_tracebacks(True)
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    rv  = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    







