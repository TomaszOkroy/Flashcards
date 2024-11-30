import logging

class ListHandler(logging.Handler): # Inherit from logging.Handler
        def __init__(self, log_list):
                # run the regular Handler __init__
                logging.Handler.__init__(self)
                # Our custom argument
                self.log_list = log_list
        def emit(self, record):
                # record.message is the log message

                self.log_list.append(self.format(record).rstrip('\n'))
logs_list = []

logger = logging.getLogger("log_list")
# specify the lowest boundary for logging
logger.setLevel(logging.DEBUG)
#create list handler
list_handler = ListHandler(logs_list)
list_handler.setFormatter(logging.Formatter('%(asctime)s | - %(levelname)s:  %(message)s'))

logger.addHandler(list_handler)


