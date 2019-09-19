# -- Function to create a monthly report -- #
def log(LogFile):
	
	import logging
	import logging.handlers

	# -- Set Up Logging -- #

	logger = logging.getLogger('reports')
	#logger.setLevel(logging.INFO)
	logger.setLevel(logging.DEBUG)
	#log_handler = logging.handlers.TimedRotatingFileHandler(LogFile, when='D', interval=1, backupCount=90)
	log_handler = logging.handlers.RotatingFileHandler(LogFile, maxBytes=10240, backupCount=10)
	log_format = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s: %(message)s')
	log_handler.setFormatter(log_format)
	logger.addHandler(log_handler)
	
	return logger
