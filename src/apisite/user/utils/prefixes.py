from . import memcached

#TODO: Connect to memcached thru socket ?
memcached_client = None

def search_people(prefix):
    global memcached_client
    if not memcached_client:
        memcached_client = memcached.connect_memcached()
    return memcached.get(memcached_client, prefix)

def search_company(prefix):
    global memcached_client
    if not memcached_client:
        memcached_client = memcached.connect_memcached()
    return memcached.get(memcached_client, "company%s" % prefix)
