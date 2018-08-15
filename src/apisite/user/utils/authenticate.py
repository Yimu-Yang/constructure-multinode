import os,binascii

from . import sqlite

TOKEN_EXPIRATION_MINS = 60

def generate_authentication_token(user_id):
    token = binascii.b2a_hex(os.urandom(15))
    with sqlite.DatabaseConnection(sqlite.token_db_path, read_only=False) as conn:
        conn.begin()
        conn.execute("INSERT INTO UserTokens (user_id, token) VALUES (?, ?);",
            (user_id, token))
        conn.commit()
    return token

def verify_authentication_token(token):
    with sqlite.DatabaseConnection(sqlite.token_db_path) as conn:
        res = conn.execute("""
            SELECT user_id
            FROM UserTokens
            WHERE (token = ?
                AND
                CURRENT_TIMESTAMP <= datetime(creation, '+'||?||' minutes')
                )
            """,
            (token, TOKEN_EXPIRATION_MINS))
        return res[0][0] if len(res) else None

def cleanup_token_db():
    with sqlite.DatabaseConnection(sqlite.token_db_path) as conn:
        conn.begin()
        conn.execute("""
            DELETE FROM UserTokens
            WHERE CURRENT_TIMESTAMP > datetime(creation, '+'||?||' minutes')
            """, (TOKEN_EXPIRATION_MINS, ))
        conn.commit()