from pymemcache.client import base

HOSTNAME = "localhost"
PORT = 8022

def connect_memcached():
	return base.Client((HOSTNAME, PORT))

def store(client, key, value):
	return client.set(key, value)

def get(client, key):
	return client.get(key)