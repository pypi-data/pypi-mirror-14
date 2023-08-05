#!/usr/bin/env python

""" This is a  program to run the flask application on Tornado Server """

import sys, re, logging
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flaskApp import application

def runLocationApp():
	
	""" FUNCTION TO RUN FLASK APPLICATION ON TORNADO SERVER FOR ASYNC REQUESTS & ERROR HANDLING """
	
	if len(sys.argv) < 2:
		print("\n\n  ARGUMENT ERROR: Port not specified\n\n  SYNTAX: python serve.py <port-number>\n\n")
		logging.info("\n\n  ARGUMENT ERROR: Port not specified\n\n  SYNTAX: python serve.py <port-number>\n\n")
	
	elif (sys.argv[1].isalpha()) == False and len(sys.argv) == 2:														# Check if arguments contain alphabets
		if int(sys.argv[1]) in range(1024, 65535):																	    # Check if port is valid
			port = sys.argv[1]
			http_server = HTTPServer(WSGIContainer(application))
			http_server.listen(port)																					# Listen on the port specified
			print("\n\n  SUCCESS: Access LocationWebApp at http://localhost:" + str(port) + "\n\n")
			logging.info("\n\n  SUCCESS: Access LocationWebApp at http://localhost:" + str(port) + "\n\n")
			IOLoop.instance().start()
			
		else:
			print("\n\n  PORT ERROR: Not a valid usable port\n\n")
			logging.info("\n\n  PORT ERROR: Not a valid usable port\n\n")
			
	elif (sys.argv[1].isalpha()) == True and len(sys.argv) == 2:
		print("\n\n  PORT ERROR: Port cannot contain an alphabet\n\n")
		logging.info("\n\n  PORT ERROR: Port cannot contain an alphabet\n\n")
	
			
	else:
		print("\n\n  ARGUMENT ERROR: Takes only one argument\n\n  SYNTAX: python serve.py <port-number>\n\n")
		logging.info("\n\n  ARGUMENT ERROR: Takes only one argument\n\n  SYNTAX: python serve.py <port-number>\n\n")

if __name__ == "__main__":
	
	logging.basicConfig(level=logging.INFO, filename="locationApp.log", format="%(asctime)s %(message)s")				# Log the stdout to locationApp.log file
	runLocationApp()
