import os,binascii

def generate_authentication_token(self, client, user_id):
    token = binascii.b2a_hex(os.urandom(15))
    memcached.store(client, 
        token, user_id)
    return token

def verify_authentication_token(self, client, token, user_id):
    try:
        expected_user_id = memcached.get(client,
            token)
        if expected_user_id != user_id:
            return False
        return True
    except:
        return False
