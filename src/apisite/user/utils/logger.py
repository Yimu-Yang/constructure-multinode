import logging

logging.basicConfig(filename='/tmp/testlogging')

def log(msg):
	logging.error(msg)

