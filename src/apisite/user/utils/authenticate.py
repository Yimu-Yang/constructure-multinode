import os,binascii

from . import sqlite

def generate_authentication_token(self, user_id):
    token = binascii.b2a_hex(os.urandom(15))
    with sqlite.DatabaseConnection(sqlite.token_db_path, read_only=False) as conn:
        conn.begin()
        conn.execute("INSERT INTO UserTokens (user_id, token) VALUES (?, ?);",
            (user_id, token))
        conn.commit()

def verify_authentication_token(self, client, token):
    with sqlite.DatabaseConnection(sqlite.token_db_path) as conn:
        res = conn.execute("SELECT user_id FROM UserTokens WHERE token = ?",
            (token,))
        return res[0][0] if len(res) else None
